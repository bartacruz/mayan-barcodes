# mayan-barcodes
Barcode scanning module for [Mayan EDMS](https://www.mayan-edms.com)

Heavily based on various apps from Mayan itself.

Uses PIL and pyzbar to scan for bar and QR codes into uploaded documents, and stores them into a Barcode object.

## Install

0. Get the code (d'oh!)
1. Add the path where you installed it to the PYTHONPATH in Mayan's scripts.
2. Activate the Mayan virtualenv
3. Install requirements (Pillow and pyzbar) with pip using requirements.txt
4. Add 'mayan_barcodes' to INSTALLED_APPS, tipically in mayan/settings/base.py or any other settings file.
5. Run migration for mayan-barcodes (manage.py migrate mayan_barcodes)

## Usage

### Configure the DocumentTypes
Go to System->Configuration->Document Types. For each DocumentType you'll see a new button called "Setup barcodes".
Setup the document types that you want to be scanned.

<img src="/docs/setup_document_type1.png" />
<img src="/docs/setup_documenttype2.png" />

And you're ready to go!

Upload a file of a type that has scanning enabled, and the scanned barcodes will be displayed in the document page.

An icon shows in the vertical toolbar 

<img src="/docs/document_barcodes1.png" style="text-align:center" />

The barcodes show in a page like this:

<img src="/docs/document_barcodes_list.png" />

### Batch Scan
In the *Tools* menu, you'll find an action called *Scan barcodes per document type*, 
very similar to the one used for OCR or process File Metadata.

It let's you choose the Document Types and then it batch process them.

### Acessing barcodes
Barcodes of a document, document version, or page are accessible via the `barcodes` tag.
<img src="/docs/sandbox.png" />
Examples:
```
# All the document barcodes
{{ document.barcodes }}
# First barcode
{{ document.barcodes.first }}
# First barcode data
{{ document.barcodes.first.data }}
# First barcode type
{{ document.barcodes.first.type }}
# The same applies to document_version
{{ document.latest_version.barcodes.first }}
{% for barcode in document.latest_version.barcodes %}Barcode {{ barcode.data }}
{% endfor %}

# Document pages `barcodes` is not a queryset but a RelatedManager, so you need to call `all()`
# if you want to access all the barcodes.
{{ document.latest_version.pages.last.barcodes.all }}
# But its the same for getting single barcodes
{{ document.latest_version.pages.last.barcodes.first }}
```


## Credits
(c) Copyroght 2020 - Julio Santa Cruz <bartacruz@gmail.com>
Released under the GPLv3 License. A copy of that licencse is in the [COPYING](COPYING) file.

Some code borrowed and then modified from the beautiful [Mayan EDMS](https://www.mayan-edms.com) which is licensed under the Apache License 2.0. 


