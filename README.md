# mayan-barcodes
Barcode scanning module for [Mayan EDMS](https://www.mayan-edms.com)

Heavily based on various apps from Mayan itself.

Uses PIL and pyzbar to scan for bar and QR codes into uploaded documents, and stores them into a Barcode object.

## Install

Install requirements (into the Mayan virtualenv) using requirements.txt

Add 'mayan-barcodes' to INSTALLED_APPS

Run migration for mayan-barcodes

## Usage

### Configure the DocumentTypes
Go to System->Configuration->Document Types. For each DocumentType you'll see a new button called "Setup barcodes".
Setup the document types that you want to be scanned.

<img src="/docs/setup_document_type1.png" />
<img src="/docs/setup_document_type2.png" />

And you're ready to go!

Upload a file of a type that has scanning enabled, and the scanned barcodes will be displayed in the document page.

<img src="/docs/document_barcodes1.png" />
<img src="/docs/document_barcodes2.png" />

### Acessing barcodes
Barcodes of a document, document version, or page are accessible via the {{{barcodes }}} tag.
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
{% endif %}}

# Document pages "barcodes" is not a queryset but a relatedmanager, so you need to cal "all()"
{{ document.latest_version.pages.last.barcodes.all }}
```

## Credits
Some code borrowed and then modified from the beautiful [Mayan EDMS](https://www.mayan-edms.com) which is licensed under Apache License 2.0. 


