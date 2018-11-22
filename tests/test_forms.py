import enum
from lxml import html
from unittest import mock

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import pytest
from werkzeug.datastructures import ImmutableMultiDict

from application.cms.models import DataSource
from application.cms.forms import DataSourceForm


class TestDataSourceForm:
    def test_can_be_populated_from_data_source_object(self):
        data_source = DataSource()
        data_source.title = "blah"

        form = DataSourceForm(obj=data_source)

        assert form.title.data == data_source.title

    def test_can_populate_data_source_object_with_submitted_data(self):
        data_source = DataSource()
        form = DataSourceForm()
        form.process(formdata=ImmutableMultiDict({"title": "blah"}))

        form.populate_obj(data_source)

        assert data_source.title == form.title.data

    def test_runs_full_validation_when_sending_to_review(self):
        form = DataSourceForm(sending_to_review=True)

        form.validate()

        assert set(form.errors.keys()) >= {
            "title",
            "type_of_data",
            "type_of_statistic_id",
            "publisher_id",
            "source_url",
            "frequency_of_release_id",
            "purpose",
        }

    def test_form_can_populate_from_a_measure_page(self, stub_measure_page):
        form = DataSourceForm(**DataSourceForm.from_measure_page(stub_measure_page))

        assert form.data == {
            "remove_data_source": None,
            "title": "DWP Stats",
            "type_of_data": ["SURVEY"],
            "type_of_statistic_id": 1,
            "publisher_id": "D10",
            "source_url": "http://dwp.gov.uk",
            "publication_date": "15th May 2017",
            "note_on_corrections_or_updates": "Note on corrections or updates",
            "frequency_of_release_other": "",
            "frequency_of_release_id": 1,
            "purpose": "Purpose of data source",
        }