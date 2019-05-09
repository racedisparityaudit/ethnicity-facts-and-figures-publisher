import pytest
from werkzeug.datastructures import ImmutableMultiDict


from application.cms.models import DataSource
from application.cms.forms import DataSourceForm, MeasureVersionForm

from tests.models import MeasureVersionFactory


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

        assert set(form.errors.keys()) == {
            "title",
            "type_of_data",
            "type_of_statistic_id",
            "publisher_id",
            "source_url",
            "frequency_of_release_id",
            "purpose",
        }


class TestMeasureVersionForm:
    def test_runs_full_validation_when_sending_to_review(self):
        form = MeasureVersionForm(is_minor_update=False, sending_to_review=True)

        form.validate()

        assert set(form.errors.keys()) == {
            "title",
            "time_covered",
            "area_covered",
            "lowest_level_of_geography_id",
            "summary",
            "measure_summary",
            "need_to_know",
            "ethnicity_definition_summary",
            "methodology",
            "external_edit_summary",
            "description",
        }

    @pytest.mark.parametrize("is_minor_update, form_should_error", ((False, False), (True, True)))
    def test_update_corrects_data_mistake_only_on_minor_versions(self, is_minor_update, form_should_error):
        form = MeasureVersionForm(is_minor_update, sending_to_review=True)

        form.validate()

        assert ("update_corrects_data_mistake" in form.errors.keys()) == form_should_error

    @pytest.mark.parametrize("is_minor_update", ((True,), (False,)))
    def test_all_fields_populate_with_data(self, is_minor_update):
        measure_version = MeasureVersionFactory.create(version="1.1", status="APPROVED")

        form = MeasureVersionForm(is_minor_update=False, sending_to_review=True, obj=measure_version)

        for field in form:
            assert (
                field.data is not None and field.data is not ""
            ), f"{field.name} should be populated from the measure version"

    def test_reference_field_not_populated_with_none(self):
        measure_version = MeasureVersionFactory.create(measure__reference=None)

        form = MeasureVersionForm(is_minor_update=False, sending_to_review=True, obj=measure_version)

        assert form.internal_reference.data == "", "Measure reference None should convert to empty string in the form"
