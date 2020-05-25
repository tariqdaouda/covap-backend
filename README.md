# Epitopes.world backend (AI for COVID-19 Vaccine)

This is the backend of https://epitopes.world. It implements the open API we use to comunicate with the database

The COVID-19 is a pandemic of humongous human and economic consequences. We have developed an AI algorithm that can help identify useful targets for a vaccine against COVID-19.

Testing vaccines is a very lengthy process and patient samples are rare, fragile and precious. By making our results public, our goal is to significantly reduce the pool of targets to be tested, thus accelerating the development of a vaccine.

the backend is written using pyramid and handles communication with ArangoDB Oasis.

## Install

* go into the root folder
* python setup.py develop

## Runing the API

pserve development.ini --reload
