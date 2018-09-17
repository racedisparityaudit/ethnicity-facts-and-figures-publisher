from flask import render_template, request, current_app, flash, url_for, redirect
from flask_login import login_required, current_user

from application.auth.models import UPDATE_MEASURE
from application.cms import cms_blueprint
from application.cms.exceptions import PageExistsException, StaleUpdateException, PageUnEditable
from application.cms.models import FrequencyOfRelease, TypeOfStatistic, LowestLevelOfGeography, Organisation
from application.cms.page_service import page_service
from application.cms.views import _diff_updates
from application.cms_autosave.forms import MeasurePageAutosaveForm
from application.utils import user_has_access, user_can


@cms_blueprint.route("/<topic>/<subtopic>/<measure>/<version>/edit_and_preview", methods=["GET"])
@login_required
@user_has_access
@user_can(UPDATE_MEASURE)
def edit_and_preview_measure_page(topic, subtopic, measure, version):

    topic_page, subtopic_page, measure_page = page_service.get_measure_page_hierarchy(topic, subtopic, measure, version)

    form = MeasurePageAutosaveForm(
        obj=measure_page,
        frequency_choices=FrequencyOfRelease,
        type_of_statistic_choices=TypeOfStatistic,
        lowest_level_of_geography_choices=LowestLevelOfGeography,
    )

    context = {
        "form": form,
        "topic": topic_page,
        "subtopic": subtopic_page,
        "measure": measure_page,
        "available_actions": measure_page.available_actions(),
        "organisations_by_type": Organisation.select_options_by_type(),
    }
    return render_template("cms_autosave/edit_and_preview_measure.html", **context)


@cms_blueprint.route("/<topic>/<subtopic>/<measure>/<version>/edit_and_preview", methods=["POST"])
@login_required
@user_has_access
@user_can(UPDATE_MEASURE)
def update_measure_page(topic, subtopic, measure, version):

    topic_page, subtopic_page, measure_page = page_service.get_measure_page_hierarchy(topic, subtopic, measure, version)

    form = MeasurePageAutosaveForm(
        obj=measure_page,
        frequency_choices=FrequencyOfRelease,
        type_of_statistic_choices=TypeOfStatistic,
        lowest_level_of_geography_choices=LowestLevelOfGeography,
    )

    form_data = form.data
    form_data["subtopic"] = request.form.get("subtopic", None)

    try:
        page_service.update_page(measure_page, data=form_data, last_updated_by=current_user.email)
        message = 'Updated page "{}"'.format(measure_page.title)
        current_app.logger.info(message)

    except StaleUpdateException as e:
        flash("Someone else updated this page whilst you were editing it, so your changes haven’t been saved. Please re-edit this page to make your changes.", "error")

    url = url_for('cms.edit_and_preview_measure_page', topic=topic_page.guid, subtopic=subtopic_page.guid, measure=measure_page.guid, version=measure_page.version)
    return redirect(url)
