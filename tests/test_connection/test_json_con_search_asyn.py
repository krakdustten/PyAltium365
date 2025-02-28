import datetime

from py_altium365.connection.json_con_search_async import (
    JsonConSearchAsync,
    JsonFacetedCounter,
    FacedType,
    SearchDataType,
    JsonDocument,
    JsonField,
    SearchDataBase,
)


def create_search_api(mocker) -> JsonConSearchAsync:
    url = "test_url"
    session_guid = "test_session_guid"
    host = "test_host"

    update = mocker.patch("py_altium365.connection.json_con_search_async.JsonConSearchAsync._update_search_names_and_counters")
    update.return_value = None

    return JsonConSearchAsync(url, session_guid, host)


def test_init(mocker):
    url = "test_url"
    session_guid = "test_session_guid"
    host = "test_host"

    update = mocker.patch("py_altium365.connection.json_con_search_async.JsonConSearchAsync._update_search_names_and_counters")
    update.return_value = None

    search = JsonConSearchAsync(url, session_guid, host)
    assert search._url == url + "/v1.0/searchasync"
    assert search._counters_up_to_date is False
    assert len(search._search_parameters) == 0
    assert len(search._search_counters) == 0
    assert search._total_hits == 0
    assert search._session_guid == session_guid
    assert search._host == host
    assert update.called


def test_add_search_parameter_new(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))

    assert search.add_search_parameter("test_name", "test_value") is True
    assert len(search._search_parameters) == 1
    assert search._search_parameters[0].item.term.field == "test_5FnameDD420E8DDD8B445E911A0601BB2B6D53"
    assert search._search_parameters[0].item.term.value == "test_value"


def test_add_search_parameter_existing(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search.add_search_parameter("test_name", "first_value")
    search.add_search_parameter("test_name", "second_value")

    assert search.add_search_parameter("test_name", "test_value") is True
    assert len(search._search_parameters) == 1
    assert len(search._search_parameters[0].item.items) == 3
    assert search._search_parameters[0].item.items[0].item.term.value == "test_value"
    assert search._search_parameters[0].item.items[1].item.term.value == "second_value"
    assert search._search_parameters[0].item.items[2].item.term.value == "first_value"


def test_add_search_parameter_existing_with_other_name(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search.add_search_parameter("test_name", "first_value")
    search.add_search_parameter("test_name", "second_value")

    assert search.add_search_parameter("test_name2", "test_value") is True
    assert len(search._search_parameters) == 2
    assert len(search._search_parameters[0].item.items) == 2
    assert search._search_parameters[1].item.term.value == "test_value"
    assert search._search_parameters[0].item.items[0].item.term.value == "second_value"
    assert search._search_parameters[0].item.items[1].item.term.value == "first_value"


def test_add_search_parameter_existing_force_remove(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search.add_search_parameter("test_name", "first_value")

    assert search.add_search_parameter("test_name", "test_value", remove_old=True) is True
    assert len(search._search_parameters) == 1
    assert search._search_parameters[0].item.term.value == "test_value"


def test_add_search_parameter_no_counter(mocker):
    search = create_search_api(mocker)

    assert search.add_search_parameter("test_name", "test_value") is False
    assert len(search._search_parameters) == 0


def test_remove_search_parameter(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search.add_search_parameter("test_name", "first_value")
    search.add_search_parameter("test_name", "second_value")

    assert search.remove_search_parameter("test_name", "first_value") is True
    assert len(search._search_parameters) == 1
    assert search._search_parameters[0].item.term.value == "second_value"


def test_get_all_search_parameters(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search.add_search_parameter("test_name", "first_value")
    search.add_search_parameter("test_name", "second_value")
    search.add_search_parameter("test_name2", "third_value")

    assert search.get_all_search_parameters() == {"test_name": ["second_value", "first_value"], "test_name2": ["third_value"]}


def test_clear_search_parameters(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search.add_search_parameter("test_name", "first_value")
    search.add_search_parameter("test_name", "second_value")
    search.add_search_parameter("test_name2", "third_value")

    search.clear_search_parameters()
    assert len(search._search_parameters) == 0


def test_add_content_search_parameter(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="ContentType", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))

    assert search.add_content_search_parameter(SearchDataType.COMPONENT) is True
    assert len(search._search_parameters) == 1
    assert search._search_parameters[0].item.term.field == "ContentTypeDD420E8DDD8B445E911A0601BB2B6D53"
    assert search._search_parameters[0].item.term.value == "Component"


def test_add_content_search_parameter_add(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="ContentType", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search.add_content_search_parameter(SearchDataType.COMPONENT)

    assert search.add_content_search_parameter(SearchDataType.DATASHEET) is True
    assert len(search._search_parameters) == 1
    assert search._search_parameters[0].item.items[0].item.term.value == "Datasheet"
    assert search._search_parameters[0].item.items[1].item.term.value == "Component"


def test_remove_content_search_parameter(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="ContentType", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search.add_content_search_parameter(SearchDataType.COMPONENT)

    assert search.remove_content_search_parameter(SearchDataType.COMPONENT) is True
    assert len(search._search_parameters) == 0


def test_add_search_parameter_range(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))

    assert search.add_search_parameter_range("test_name", 2.0, 4.0) is True
    assert len(search._search_parameters) == 1
    assert search._search_parameters[0].item.field == "test_5FnameDD420E8DDD8B445E911A0601BB2B6D53"
    assert search._search_parameters[0].item.min == 2.0
    assert search._search_parameters[0].item.max == 4.0
    assert search._search_parameters[0].item.min_inclusive is True
    assert search._search_parameters[0].item.max_inclusive is True


def test_add_search_parameter_range_no_counter(mocker):
    search = create_search_api(mocker)

    assert search.add_search_parameter_range("test_name", 2.0, 4.0) is False
    assert len(search._search_parameters) == 0


def test_add_search_parameter_range_no_support(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=False))

    assert search.add_search_parameter_range("test_name", 2.0, 4.0) is False
    assert len(search._search_parameters) == 0


def test_remove_search_parameter_range(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))
    search.add_search_parameter_range("test_name", 2.0, 4.0)

    assert search.remove_search_parameter_range("test_name") is True
    assert len(search._search_parameters) == 0


def test_get_search_parameter_range(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))
    search.add_search_parameter_range("test_name", 2.0, 4.0)

    assert search.get_search_parameter_range("test_name") == (2.0, 4.0, True, True)


def test_get_search_parameter_range_not_found(mocker):
    search = create_search_api(mocker)

    assert search.get_search_parameter_range("test_name") is None


def test_get_all_search_parameters_range(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))
    search.add_search_parameter_range("test_name", 2.0, 4.0)
    search.add_search_parameter_range("test_name2", 3.0, 5.0)

    assert search.get_all_search_parameters_range() == {"test_name": (2.0, 4.0, True, True), "test_name2": (3.0, 5.0, True, True)}


def test_clear_search_parameters_range(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))
    search.add_search_parameter_range("test_name", 2.0, 4.0)
    search.add_search_parameter_range("test_name2", 3.0, 5.0)

    search.clear_search_parameters_range()
    assert len(search._search_parameters) == 0


def test_add_search_parameter_wildcard(mocker):
    search = create_search_api(mocker)

    assert search.add_search_parameter_wildcard("test_name") is True
    assert len(search._search_parameters) == 1
    assert search._search_parameters[0].item.items[0].item.term.field == "TextC623975962814A5FAAD7FA1CD85DA0DB"
    assert search._search_parameters[0].item.items[0].item.term.value == "test_name"
    assert search._search_parameters[0].item.items[1].item.term.field == "DynamicDataC623975962814A5FAAD7FA1CD85DA0DB"
    assert search._search_parameters[0].item.items[1].item.term.value == "test_name"


def test_add_search_parameter_wildcard_overwrite(mocker):
    search = create_search_api(mocker)

    search.add_search_parameter_wildcard("test_name")
    assert search.add_search_parameter_wildcard("test_name2") is True
    assert len(search._search_parameters) == 1
    assert search._search_parameters[0].item.items[0].item.term.value == "test_name2"
    assert search._search_parameters[0].item.items[1].item.term.value == "test_name2"


def test_get_search_parameter_wildcard(mocker):
    search = create_search_api(mocker)

    search.add_search_parameter_wildcard("test_name")
    assert search.get_search_parameter_wildcard() == "test_name"


def test_get_search_parameter_wildcard_not_found(mocker):
    search = create_search_api(mocker)

    assert search.get_search_parameter_wildcard() is None


def test_get_current_count(mocker):
    search = create_search_api(mocker)

    search._total_hits = 10
    assert search.get_current_count() == 10


def test_get_all_search_names_and_type(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))

    assert search.get_all_search_names_and_type() == [("test_name", FacedType.NO_TYPE), ("test_name2", FacedType.NO_TYPE)]


def test_get_all_search_names(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[]))

    assert search.get_all_search_names() == ["test_name", "test_name2"]


def test_get_all_search_names_range(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))

    assert search.get_all_search_names() == ["test_name", "test_name2"]


def test_get_all_search_names_and_type_range(mocker):
    search = create_search_api(mocker)

    search._search_counters.append(JsonFacetedCounter(FacetName="test_name", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))
    search._search_counters.append(JsonFacetedCounter(FacetName="test_name2", faced_type=FacedType.NO_TYPE, TotalHitCount=0, Counters=[], SupportRange=True))

    assert search.get_all_search_names_and_type_range() == [("test_name", FacedType.NO_TYPE), ("test_name2", FacedType.NO_TYPE)]


def test_get_results(mocker):
    search = create_search_api(mocker)

    scom = mocker.Mock()
    scom.return_value.success = True
    scom.return_value.documents = [
        JsonDocument(
            Score=1.0,
            Fields=[
                JsonField(Name="test_name", Value="test_value"),
                JsonField(Name="test_name2", Value="test_value2"),
                JsonField(Name="CreatedAt", Value="0.41451"),
                JsonField(Name="LatestRevision", Value="0"),
            ],
        ),
        JsonDocument(
            Score=1.0,
            Fields=[
                JsonField(Name="test_name4", Value="test_value4"),
                JsonField(Name="test_name5", Value="test_value5"),
                JsonField(Name="CreatedAt", Value="5/5/2021 12:00:00"),
            ],
        ),
    ]
    search._send_command = scom

    assert search.get_results() == [
        SearchDataBase(
            Parameters={"test_name": "test_value", "test_name2": "test_value2"},
            CreatedAt=datetime.datetime(1899, 12, 31, 9, 56, 53, 664000),
            LatestRevision=False,
        ),
        SearchDataBase(Parameters={"test_name4": "test_value4", "test_name5": "test_value5"}, CreatedAt=datetime.datetime(2021, 5, 5, 12, 0)),
    ]
