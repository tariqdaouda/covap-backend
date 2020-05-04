import pyArango.collection as COL
import pyArango.validation as VAL

class VirusSequences(COL.Collection):

  #_properties = {
  #    "keyOptions" : {
  #        "allowUserKeys": False,
  #        "type": "autoincrement",
  #        "increment": 1,
  #        "offset": 0,
  #    }
  #}

  _validation = {
      'on_save': True,
      'on_set': True,
      'allow_foreign_fields': True
  }

  _fields = {
      "Index": COL.Field(validators=[VAL.NotNull()]),
      'Accession': COL.Field(validators=[VAL.NotNull()]),
      'Sequence': COL.Field(validators=[VAL.NotNull()]),
      'Version': COL.Field(),
      'Sub_accession': COL.Field(),
      'Protein_accession': COL.Field(),
      'Release_Date': COL.Field(),
      'Genus': COL.Field(),
      'Family': COL.Field(),
      'Length': COL.Field(),
      'Nuc_Completeness': COL.Field(),
      'Genotype': COL.Field(),
      'Genome_Region': COL.Field(),
      'Segment': COL.Field(),
      'Authors': COL.Field(),
      'Publications': COL.Field(),
      'Geo_Location': COL.Field(),
      'Host': COL.Field(),
      'Authors': COL.Field(),
      'Isolation_Source': COL.Field(),
      'Collection_Date': COL.Field(),
      'BioSample': COL.Field(),
      'GenBank_Title': COL.Field(),
  }

  _field_types = {
      'Index': 'floar',
      'Accession': "enumeration",
      # 'Sequence': "enumeration",
      'Version': "enumeration",
      'Sub_accession': "enumeration",
      'Protein_accession': "enumeration",
      'Release_Date': "enumeration",
      'Genus': "enumeration",
      'Family': "enumeration",
      'Length': "float",
      'Nuc_Completeness': "enumeration",
      'Genotype': "enumeration",
      # 'Authors': COL.Field(),
      # 'Publications': COL.Field(),
      'Geo_Location': "enumeration",
      'Host': "enumeration",
      'Isolation_Source': "enumeration",
      'Collection_Date': "enumeration",
      'BioSample': "enumeration",
      'GenBank_Title': "enumeration",
  }

class Peptides(COL.Collection):

  #_properties = {
  #    "keyOptions" : {
  #        "allowUserKeys": False,
  #        "type": "autoincrement",
  #        "increment": 1,
  #        "offset": 0,
  #    }
  #}

  _validation = {
      'on_save': True,
      'on_set': True,
      'allow_foreign_fields': True
  }

  _fields = {
      "Index": COL.Field(validators=[VAL.NotNull()]),
      "Method": COL.Field(validators=[VAL.NotNull()]),
      "Context_size": COL.Field(validators=[VAL.NotNull()]),
      "Model_run": COL.Field(validators=[VAL.NotNull()]),
      "Accession": COL.Field(validators=[VAL.NotNull()]),
      "Sub_accession": COL.Field(validators=[VAL.NotNull()]),
      #"Position": COL.Field(validators=[VAL.NotNull()]),
      "Position": COL.Field(),  # temporarily
      "Length": COL.Field(validators=[VAL.NotNull()]),
      "Sequence": COL.Field(validators=[VAL.NotNull()]),
      "Score": COL.Field(validators=[VAL.NotNull()]),
      "Name": COL.Field(validators=[VAL.NotNull()])
  }

  _field_types = {
      "Index": "float",
      "Method": "enumeration",
      "Context_size": "enumeration",
      "Model_run": "enumeration",
      "Accession": "enumeration",
      "Sub_accession": "enumeration",
      "Position": "float",
      "Length": "enumeration",
      "Score": "float",
      "Sequence": "enumeration",
      "Name": "enumeration"
  }

__COLLECTIONS = { col.__name__: col for col in [VirusSequences, Peptides] }
