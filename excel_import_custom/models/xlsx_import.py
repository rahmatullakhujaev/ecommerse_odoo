from odoo import fields, models
import base64
import uuid
from ast import literal_eval
from datetime import date, datetime as dt
from io import BytesIO

import xlrd
import xlwt

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.safe_eval import safe_eval

from . import common as co


class ExcelImport(models.Model):
    _inherit = "xlsx.import"

    @api.model
    def _import_record_data(self, import_file, record, data_dict):
        """From complex excel, create temp simple excel and do import"""
        if not data_dict:
            return
        try:
            header_fields = []
            model = record._name
            decoded_data = base64.decodebytes(import_file)
            wb = xlrd.open_workbook(file_contents=decoded_data)
            out_wb = xlwt.Workbook()
            out_st = out_wb.add_sheet("Sheet 1")
            xml_id = (
                    record
                    and self.get_external_id(record)
                    or "{}.{}".format("__excel_import_export__", uuid.uuid4())
            )
            out_st.write(0, 0, "id")  # id and xml_id on first column
            out_st.write(1, 0, xml_id)
            header_fields.append("id")
            # Process on all worksheets
            self._process_worksheet(wb, out_wb, out_st, model, data_dict, header_fields)
            # --
            content = BytesIO()
            out_wb.save(content)
            content.seek(0)  # Set index to 0, and start reading
            xls_file = content.read()
            # Do the import
            Import = self.env["base_import.import"]
            imp = Import.create(
                {
                    "res_model": model,
                    "file": xls_file,
                    "file_type": "application/vnd.ms-excel",
                    "file_name": "temp.xls",
                }
            )
            errors = imp.execute_import(
                header_fields,
                header_fields,
                {
                    "has_headers": True,
                    "advanced": True,
                    "keep_matches": False,
                    "encoding": "",
                    "separator": "",
                    "quoting": '"',
                    "date_format": "%Y-%m-%d",
                    "datetime_format": "%Y-%m-%d %H:%M:%S",
                    "float_thousand_separator": ",",
                    "float_decimal_separator": ".",
                    "fields": [],
                },
            )
            if errors.get("messages"):
                message = _("Error importing data")
                messages = errors["messages"]
                if isinstance(messages, dict):
                    message = messages["message"]
                if isinstance(messages, list):
                    message = ", ".join([x["message"] for x in messages])
                raise ValidationError(message.encode("utf-8"))
            return self.env.ref(xml_id)
        except xlrd.XLRDError as exc:
            raise ValidationError(
                _("Invalid file style, only .xls or .xlsx file allowed")
            ) from exc
        except Exception as e:
            raise e
