import wepitope.models.db_collections as COL
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
      accession = list(set(re.findall("NC_[0-9]+", header)))[0]
      if ".." in header :
        sub_accession = header.split("|")
        sub_accession = "|".join(sub_accession[:-2])[1:]#.join("|")
      else:
        sub_accession = accession

      try :
        accession_version = list(set(re.findall("\.([0-9]+):", header)))[0]
      except IndexError:
        accession_version=None

      try :
        protein_accession = list(set(re.findall("[Y|N]P_[0-9]+", header)))[0]
      except IndexError:
        protein_accession=None
      
      return {
        "Accession": accession,
        "Version": accession_version,
        "Sub_accession": sub_accession,
        "Protein_accession": protein_accession
      }

    print("loading meta...")
    meta_df = pd.read_csv(metadata, sep=",")
    print(meta_df.head())

    entries = {}
    for file in (genome_sequences, cds_sequences):
      fasta = FastaFile()
      fasta.parseFile(file)
      for seq in fasta:
        header_info = _parse_fasta_header(seq[0])
        accession = header_info["Accession"]
        entries[accession] = header_info
        
        sequence = seq[1].replace("\n", "").replace("\r", "")
        entries[accession]["Sequence"] = sequence
        entries[accession]["Length"] = len(sequence)
        meta_line = self._line_to_dct(meta_df[meta_df.Accession == accession].set_index("Accession"))
        if meta_line is None :
          print(entries[accession], meta_df.Accession == accession)
          print(meta_df)
          stop
        entries[accession].update(meta_line)
    
    print("saving sequences...")
    self.db["VirusSequences"].bulkSave(entries.values())
    print("\tsaved:", len(entries))

    print("building indexes...")
    for name, typ in COL.VirusSequences._field_types.items():
      if name == "Accession" or name == "Sub_accession":
        self.db["VirusSequences"].ensureHashIndex([name], unique=True)
      elif typ == "enumeration":
        self.db["VirusSequences"].ensureHashIndex([name], unique=False, sparse=True, deduplicate=False, name=None)
      elif typ == "float":
        self.db["VirusSequences"].ensureSkiplistIndex([name], unique=False, sparse=True, deduplicate=False, name=None)

  def populate_peptides(self, predictions, save_freq=10000):
    print("saving entries...")
    preds = pd.read_csv(predictions, sep="\t")
    entries = []
    for index, row in preds.iterrows():
      dct = row.to_dict()
      new_entry = self.db["Peptides"].createDocument()
      new_entry.set(dct)
      new_entry["Accession"] = list(set(re.findall("NC_[0-9]+", dct["Sub_accession"])))[0]
      entries.append(new_entry)
      
      if index > 0 and index % save_freq == 0:
        self.db["Peptides"].bulkSave(entries)
        entries = []

    self.db["Peptides"].bulkSave(entries)
    print("building indexes...")
    self.db["VirusSequences"].ensureHashIndex(["Sequence"], unique=False, sparse=True, deduplicate=False, name=None)
    for name, typ in COL.VirusSequences._field_types.items():
      if typ == "enumeration":
        self.db["VirusSequences"].ensureHashIndex([name], unique=False, sparse=True, deduplicate=False, name=None)
      elif typ == "float":
        self.db["VirusSequences"].ensureSkiplistIndex([name], unique=False, sparse=True, deduplicate=False, name=None)

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
