from src.tags.schemas import TagCreateModel

tags_prefix = "api/v1/tag"


def test_get_all_tags(test_client, fake_tag_service, fake_session):
    response = test_client.get(
        url=f"{tags_prefix}"
    )
    
    assert fake_tag_service.get_all_tags_called_once()
    assert fake_tag_service.get_all_tags_called_once_with(fake_session)
    
    
def test_user_creation(fake_session, fake_tag_service, test_client):
    tag_data = {"name": "api_python"}
    
    response = test_client.post(
        url=f"{tags_prefix}/signup",
        json=tag_data
    )
    
    tag_data = TagCreateModel(**tag_data)
    
    assert fake_tag_service.create_tag_called_once()
    assert fake_tag_service.create_tag_called_once_with(tag_data, fake_session)