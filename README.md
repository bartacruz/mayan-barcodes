# mayan-barcodes
Barcode scanning module for [Mayan EDMS](https://www.mayan-edms.com)

Heavily based on various apps from Mayan itself.

Uses PIL and pyzbar to scan for bar and QR codes into uploaded documents, and stores them into a Barcode object.

## Install

Install requirements (into the Mayan virtualenv) using requirements.txt

Add 'mayan-barcodes' to INSTALLED_APPS

Run migration for mayan-barcodes

## Usage

Configure the DocumentTypes that will be scanned.
Go to System->Configuration->Document Types. For each DocumentType you'll see a new button called "Setup barcodes"

And you're ready to go!

Upload a file of a type that has scanning enabled, and the scanned barcodes will be accesible.

## Credits
Some code borrowed and then modified from the beautiful [Mayan EDMS](https://www.mayan-edms.com) which is licensed under Apache License 2.0. 


