import collections as COL

import pyArango.connection as CON

class Populater(object):
  """docstring for Populater"""
  def __init__(self, url, username, password):
    super(Populater, self).__init__()
    self. conn = CON.Connection(
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
      self.db = self.conn.createDatabase("covap")
    except :
      print("Database already exists")
    
    # for colname in ("VirusSequences", "Peptides"):
    for colname in ("Entries"):
      try :
        self.db.createCollection(COL.VirusSequences)
      except :
        print("Collection %s already exists" % colname)

  def populate(self, metadata, genome_sequences, cds_sequences, predictions):
    import pandas as pd
    from pyGeno.tools.parsers.FastaTools import FastaFile

    print("loading meta...")
    meta = pd.read_csv(metadata, sep="\t"):
    meta.set_index("Accession")

    print("loading sequences...")
    sequences = {}
    for file in (genome_sequences, cds_sequences):
      for seq in FastaFile().parse(genome_sequences):
        accession = seq.header.split("|")[0].strip()
        sequence = seq.sequence.replace("\n", "").replace("\r", "")
        sequence[accession] = {"Sequence": sequence}
        sequence[accession].update(meta[accession].to_dict())
    
    print("saving entries...")
    preds = pd.read_csv(predictions, sep="\t"):
    for line in preds.rows():
      dct = line.to_dict()
      dct.update(
        sequence[dct["accession"]]    
      )
      new_entry = self.db["Entries"].createDocument().set(dct)
      new_entry.save()

    print("done.")

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
  pop.populate(metadata, genome_sequences, cds_sequences, predictions)

if __name__ == '__main__':
  populate()
