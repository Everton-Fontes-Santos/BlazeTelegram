from blazetelegrambot.domain.factory.event_factory import EventFactory

from datetime import datetime


async def test_create_event():
    date_string = '2023-08-09 00:00:00'
    time = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    factory = EventFactory()
    
    updated_event = factory.create(
        name='updated',
        data='hello',
        occured=time
    )
    updated_event2 = await factory.create_and_publish(
        name='updated',
        data='hello',
        occured=date_string
    )
    
    assert updated_event.name == 'updated'
    assert updated_event.data == 'hello'
    assert updated_event.ocurred.time() == time.time()
    assert updated_event2.ocurred.time() == time.time()