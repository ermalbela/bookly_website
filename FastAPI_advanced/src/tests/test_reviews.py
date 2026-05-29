reviews_prefix = "api/v1/review"


def test_get_all_reviews(test_client, fake_tag_service, fake_session):
    response = test_client.get(
        url=f"{reviews_prefix}"
    )
    
    assert fake_tag_service.get_all_reviews_called_once()
    assert fake_tag_service.get_all_reviews_called_once_with(fake_session)