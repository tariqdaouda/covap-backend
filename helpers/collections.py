import pyArango.collection as COL

class Entries(COL.Collection):

  # _properties = {
  #     "keyOptions" : {
  #         "allowUserKeys": False,
  #         "type": "autoincrement",
  #         "increment": 1,
  #         "offset": 0,
  #     }
  # }

  _validation = {
      'on_save': True,
      'on_set': True,
      'allow_foreign_fields': True
  }

  _fields = {
      'Accession': Field(validators=[VAL.NotNull()]),
      'Sequence': Field(validators=[VAL.NotNull()]),
      'Release_Date': Field(),
      'Genus': Field(),
      'Family': Field(),
      'Length': Field(),
      'Nuc_Completeness': Field(),
      'Genotype': Field(),
      'Genome_Region': Field(),
      'Segment': Field(),
      'Authors': Field(),
      'Publications': Field(),
      'Geo_Location': Field(),
      'Host': Field(),
      'Authors': Field(),
      'Isolation_Source': Field(),
      'Collection_Date': Field(),
      'BioSample': Field(),
      'GenBank_Title': Field(),
      'Coding': Field(),
      'Position': Field(),
      'Peptide_Sequence': Field(validators=[VAL.NotNull()]),
      'Peptide_Position': Field(validators=[VAL.NotNull()]),
      'Peptide_Score': Field(validators=[VAL.NotNull()]),
      'Peptide_Length': Field(validators=[VAL.NotNull()]),
  }

  _field_types = {
      'Accession': "other",
      'Sequence': "other",
      'Release_Date': "date",
      'Genus': "enumeration",
      'Family': "enumeration",
      'Length': "float",
      'Nuc_Completeness': "enumeration",
      'Genotype': "enumeration",
      'Genome_Region': "enumeration",
      'Segment': "enumeration",
      'Authors': "enumeration",
      'Publications': "enumeration",
      'Geo_Location': "enumeration",
      'Host': "enumeration",
      'Authors': "enumeration",
      'Isolation_Source': "enumeration",
      'Collection_Date': "enumeration",
      'BioSample': "enumeration",
      'GenBank_Title': "enumeration",
      'Coding': "enumeration",
      'Position': "enumeration",
      'Peptide_Sequence': "other",
      'Peptide_Position': "other",
      'Peptide_Score': "float",
      'Peptide_Length': "enumeration",
  }

# class Peptide(COL.Collection):

#   _validation = {
#       'on_save': True,
#       'on_set': True,
#       'allow_foreign_fields': False
#   }

#   _fields = {
#     'Genome_Accession': Field(validators=[VAL.NotNull()]),
#     'Sequence': Field(validators=[VAL.NotNull()]),
#     'Position': Field(validators=[VAL.NotNull()]),
#     'Score': Field(validators=[VAL.NotNull()]),
#     'Length': Field(validators=[VAL.NotNull()]),
#   }

#   class VirusSequence(COL.Collection):

#   _validation = {
#       'on_save': True,
#       'on_set': True,
#       'allow_foreign_fields': False
#   }

#   _fields = {
#       'Accession': Field(validators=[VAL.NotNull()]),
#       'Sequence': Field(validators=[VAL.NotNull()]),
#       'Release_Date': Field(),
#       'Genus': Field(),
#       'Family': Field(),
#       'Length': Field(),
#       'Nuc_Completeness': Field(),
#       'Genotype': Field(),
#       'Genome_Region': Field(),
#       'Segment': Field(),
#       'Authors': Field(),
#       'Publications': Field(),
#       'Geo_Location': Field(),
#       'Host': Field(),
#       'Authors': Field(),
#       'Isolation_Source': Field(),
#       'Collection_Date': Field(),
#       'BioSample': Field(),
#       'GenBank_Title': Field(),
#       'Coding': Field(),
#       'Position': Field()
#   }
