from model import *


def doc_to_object(doc):
    items = []
    for item in doc.items:
        items.append({
            'name': item.name,
            'amount': item.amount,
            'unit': item.unit,
            'price': item.price
        })

    return {
        'number': doc.number,
        'due_date': doc.due_date,
        'issue_date': doc.issue_date,
        'delivery_date': doc.delivery_date,

        'contractor': {
            'name': doc.contractor.name,
            'address': doc.contractor.address,
            'ico': doc.contractor.ico,
            'dic': doc.contractor.dic,
            'icdph': doc.contractor.icdph,
            'phone': doc.contractor.phone,
            'email': doc.contractor.email,
            'signature': doc.contractor.signature
        },
        'bank_account': {
            'iban': doc.bank_account.iban,
            'swift': doc.bank_account.swift
        },
        'currency': doc.currency,

        'client': {
            'name': doc.client.name,
            'address': doc.client.address,
            'ico': doc.client.ico,
            'dic': doc.client.dic,
            'icdph': doc.client.icdph,
            'price': doc.client.price
        },
        'discount': doc.discount,
        'items': items
    }


def object_to_doc(obj):
    items = []
    for i in obj['items']:
        items.append(Item(i['name'], i['amount'], i['unit'], i['price']))

    return Document(
        number=obj['number'],

        issue_date=obj['issue_date'],
        delivery_date=obj['delivery_date'],
        due_date=obj['due_date'],

        contractor=Contractor(obj['contractor']),
        currency=obj['currency'],
        bank_account=BankAccount(obj['bank_account']),

        client=Client(obj['client']),
        discount=obj['discount'],
        items=items
    )
