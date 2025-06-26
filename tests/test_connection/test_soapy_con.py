from py_altium365.connection.soapy_con import SoapyCon, SoapMethod, SoapResponse, SoapHeader


def test_send_command(mocker):
    mock_session = mocker.Mock()
    mock_session.post.return_value.status_code = 200
    mock_session.post.return_value.text = """<?xml version="1.0" encoding="utf-8"?>
    <soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">
        <soap-env:Body>
            <Response xmlns="http://tempuri.org/">
                <Message xmlns="http://www.w3.org/2001/XMLSchema-instance">message_test</Message>
            </Response>
        </soap-env:Body>
    </soap-env:Envelope>
    """.replace(
        "    ", ""
    )

    soapy_con = SoapyCon(mock_session, "test_url")
    ret = soapy_con._send_command(
        SoapHeader(),
        SoapMethod(),
        SoapResponse,
    )

    assert ret.message == "message_test"
    assert mock_session.post.called
    assert mock_session.post.call_args[0][0] == "test_url"
    assert mock_session.post.call_args[1]["headers"]["content-type"] == "text/xml"
    assert mock_session.post.call_args[1]["headers"]["SOAPAction"] == "Method"
    assert mock_session.post.call_args[1]["headers"]["User-Agent"] == "Altium Designer"
    print(mock_session.post.call_args[1]["data"])
    # For some reason the XML is not always the same but the content is the same
    assert mock_session.post.call_args[1]["data"] in [
        """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Header/>
            <soap:Body>
                <Method xmlns="http://tempuri.org/"/>
            </soap:Body>
        </soap:Envelope>
        """.replace(
            "\n", ""
        )
        .replace("    ", "")
        .encode("utf-8"),
        """
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:temp="http://tempuri.org/">
            <soap:Header />
            <soap:Body>
                <temp:Method />
            </soap:Body>
        </soap:Envelope>
        """.replace(
            "\n", ""
        )
        .replace("    ", "")
        .encode("utf-8"),
    ]
