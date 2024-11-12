import os.path
from typing import List, Dict, Iterator
from pathlib import Path

from PyPDF2 import PdfWriter, PdfReader
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QApplication

from pathvalidate import validate_filepath, ValidationError, validate_filename
import fitz

from enums.message_type import MessageType
from interfaces.i_viewmodel import IViewModel, IViewModelMeta
from managers.message_manager import MessageManager


class DocumentItem:
    __document_index: int = -1

    def __init__(self, document_name: str, document_path: str, document_is_included: bool = True):
        self.document_index = DocumentItem.increase_index()
        self.document_name = document_name
        self.document_path = document_path
        self.document_is_included = document_is_included

    # <editor-fold desc="[+] Index operations">

    @classmethod
    def increase_index(cls) -> int:
        cls.__document_index += 1
        return cls.__document_index

    @classmethod
    def decrease_index(cls) -> int:
        cls.__document_index -= 1
        return cls.__document_index

    @classmethod
    def number_of_documents(cls) -> int:
        return cls.__document_index + 1

    # </editor-fold>


class MergeViewModel(QObject, IViewModel, metaclass=IViewModelMeta):
    def __init__(self):
        super().__init__()

        self.document_item_list: List[DocumentItem] = list()

    def on_pdf_paths_selected(self, pdf_paths: List[str]):
        # Set cursor to waiting
        QApplication.setOverrideCursor(Qt.WaitCursor)

        number_of_documents_before_addition = DocumentItem.number_of_documents()
        added_items = list()

        for pdf_path in pdf_paths:
            item = DocumentItem(Path(pdf_path).stem, pdf_path)
            added_items.append(item)
            print("ADD", item.document_name, item.document_index)
            self.document_item_list.append(item)

        print(added_items)

        MessageManager.send(MessageType.ADD_DOCUMENT, document_items=added_items)

        # Reset cursor to default
        QApplication.restoreOverrideCursor()

    def remove_document(self, document_index: int):
        #print(document_index, self.document_item_list)

        for document in self.document_item_list[document_index + 1:]:
            document.document_index -= 1

        self.document_item_list.pop(document_index)
        DocumentItem.decrease_index()

        MessageManager.send(MessageType.MERGE_VIEWMODEL__DOCUMENT_REMOVED, document_index)

    def merge_documents(self, pdf_filename: str):
        """

        :param pdf_filename:
        :return:
        """

        # Set cursor to waiting
        QApplication.setOverrideCursor(Qt.WaitCursor)

        pdf_merged = fitz.open()

       # print("?X?")

        included_document_items: List[DocumentItem] = list(filter(lambda document: document.document_is_included, self.document_item_list))
        print("IC", included_document_items)

        if not any(included_document_items):
            print("[!] No documents")
            QApplication.restoreOverrideCursor()
            return

        print("HI!")
        for document_item in included_document_items:
            pdf_to_insert = fitz.open(document_item.document_path)
            pdf_merged.insert_pdf(pdf_to_insert)

        if pdf_filename == "":
            pdf_filename = "MIXED.pdf"

        try:
            validate_filename(pdf_filename)
        except ValidationError as e:
            print(f"{e}\n")

        name, ext = os.path.splitext(pdf_filename)

        if ext != ".pdf":
            pdf_filename = name + ".pdf"

        if os.path.isfile(pdf_filename):
            print("[!] File exists")
            QApplication.restoreOverrideCursor()
            return

        pdf_merged.save(pdf_filename)

        # Reset cursor to default
        QApplication.restoreOverrideCursor()

    def reorder_documents(self, source_index, destination_index):
        print(source_index, destination_index)
        #for doc in self.document_item_list:
       #     print(doc.document_name, doc.document_path)
       # print()
        element = self.document_item_list.pop(destination_index)
      #  for doc in self.document_item_list:
       #     print(doc.document_name, doc.document_path)
       # print()
        self.document_item_list.insert(source_index, element)

        for doc in self.document_item_list:
            print(doc.document_name, doc.document_path)
