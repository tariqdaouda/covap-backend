try :
  from . import db_collections as COL
except :
  import db_collections as COL

import pyArango.theExceptions as PEXP
import pyArango.connection as CON
import re
import pandas as pd
import click


class Populater(object):
  """docstring for Populater"""
  def __init__(self, url, username, password):
    super(Populater, self).__init__()
    self.conn = CON.Connection(
      arangoURL = url,
      username = username,
      password = password,
      verify = True,
      verbose = False,
      statsdClient = None,
      reportFileName = None,
      loadBalancing = "round-robin",
      use_grequests = False,
      use_jwt_authentication=False,
      use_lock_for_reseting_jwt=True,
      max_retries=5
    )

  def set_database(self):
    try :
      self.db = self.conn.createDatabase("Covap")
    except Exception as e :
      print("Unable to create database: %s" % e)
      self.db = self.conn["Covap"]

    for colname in ("Peptides", "VirusSequences"):
      try :
        self.db.createCollection(colname)
      except PEXP.CreationError as e :
        print("Unable to create collection '%s' : %s" % (colname, e))


  def _line_to_dct(self, line):
    import numpy as np

    if line.empty:
      return None

    line = line.replace({np.nan: None})
    line = line.to_dict(orient="list")
    for key, val in line.items():
      line[key] = val[0]
    return line

  def populate_viruses(self, metadata, genome_sequences, cds_sequences):
    from pyGeno.tools.parsers.FastaTools import FastaFile

    def _parse_fasta_header(header):
      # accession = list(set(re.findall("[>|\(]([A-Z]{2}_[0-9]+)", header)))[0]
      accession = re.findall("(NC_[0-9]+(\.[0-9]+)?)", header)[0][0].strip()

      try:
        accession, accession_version = accession.split('.')
      except ValueError:
        accession_version = None

      location = re.findall("(NC_.+?)(\||$)", header)[0][0].strip()

      try :
        protein_accession = re.findall("([Y|N]P_[0-9]+(\.[0-9]+)?)", header)[0][0].strip()
      except IndexError:
        protein_accession = None

      if not protein_accession is None:
        sub_accession = 'CDS_of_' + protein_accession
      else:
        sub_accession = location

      return {
        "Accession": accession,
        "Version": accession_version,
        "Sub_accession": sub_accession,
        "Protein_accession": protein_accession,
        "Location": location
      }

    print("loading meta...")
    meta_df = pd.read_csv(metadata, sep="\t")
    print(meta_df.head())

    entries = {}
    index = 0
    for file in (genome_sequences, cds_sequences):
      fasta = FastaFile()
      fasta.parseFile(file)
      for seq in fasta:
        header_info = _parse_fasta_header(seq[0])
        accession = header_info["Accession"].strip()
        if not header_info["Protein_accession"] is None:
            unique_accession = header_info["Protein_accession"].strip()
        else:
            unique_accession = accession
        entries[unique_accession] = header_info

        sequence = seq[1].replace("\n", "").replace("\r", "")
        entries[unique_accession]["Sequence"] = sequence
        entries[unique_accession]["Length"] = len(sequence)
        meta_line = self._line_to_dct(meta_df[meta_df.Accession == accession].set_index("Accession"))
        entries[unique_accession].update(meta_line)
        entries[unique_accession]["Index"] = index
        index += 1

    print("saving sequences...")
    self.db["VirusSequences"].bulkSave(entries.values())
    print("\tsaved:", len(entries))

    print("building indexes...")
    for name, typ in COL.VirusSequences._field_types.items():
      if name == "Sub_accession":
        self.db["VirusSequences"].ensureHashIndex([name], unique=True)
      elif typ == "enumeration":
        self.db["VirusSequences"].ensureHashIndex([name], unique=False, sparse=True, deduplicate=False, name=None)
      elif typ == "float":
        self.db["VirusSequences"].ensureSkiplistIndex([name], unique=False, sparse=True, deduplicate=False, name=None)

  def populate_peptides(self, predictions, save_freq=10000):
    import numpy as np

    print("saving entries...")
    preds = pd.read_csv(predictions, sep="\t", low_memory=False).rename({
        'Peptide_start_one_based': 'Position',
        'Peptide_length': 'Length',
        'Peptide_sequence': 'Sequence'}, axis=1).replace({np.nan:None})
    entries = []
    for index, row in preds.iterrows():
      db_keys = [x for x in self.db["Peptides"]._fields.keys() if x != 'Index']
      dct = row[db_keys].to_dict()
      new_entry = self.db["Peptides"].createDocument()
      new_entry.set(dct)
      new_entry["Index"] = index
      #new_entry["Accession"] = list(set(re.findall("NC_[0-9]+", dct["Sub_accession"])))[0].strip()
      entries.append(new_entry)

      if index > 0 and index % save_freq == 0:
        print("\tsaving: %d..." % save_freq)
        self.db["Peptides"].bulkSave(entries)
        entries = []

    print("\tsaving remaining...")
    self.db["Peptides"].bulkSave(entries)
    print("\tsaved total: %d" % (index+1))

    print("building indexes...")
    self.db["Peptides"].ensureHashIndex(["Sequence"], unique=False, sparse=True, deduplicate=False, name=None)
    for name, typ in COL.Peptides._field_types.items():
      if typ == "enumeration":
        self.db["Peptides"].ensureHashIndex([name], unique=False, sparse=True, deduplicate=False, name=None)
      elif typ == "float":
        self.db["Peptides"].ensureSkiplistIndex([name], unique=False, sparse=True, deduplicate=False, name=None)

    print("done.")

  def truncate(self):
    for colname in ("Peptides", "VirusSequences"):
      self.db[colname].truncate()

@click.command()
@click.option('--url', help='arangodb url')
@click.option('--username', help='username for the db')
@click.option('--password', help='password for the db')
@click.option('--metadata', help='tsv containing metadata')
@click.option('--genome_sequences', help='fasta containing whole genomes')
@click.option('--cds_sequences', help='fasta containing cds sequences')
@click.option('--predictions', help='tsv containing prediction results')
def populate(url, username, password, metadata, genome_sequences, cds_sequences, predictions):
  pop = Populater(url, username, password)
  pop.set_database()
  pop.truncate()
  pop.populate_viruses(metadata, genome_sequences, cds_sequences)
  pop.populate_peptides(predictions)

if __name__ == '__main__':
  populate()
