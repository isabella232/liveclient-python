import copy

from unittest import mock

from testbase import *

from live_client.events import annotation
from predicates import *
from mocks import *
from utils import settings as S


class TestCreate:
    def test_annotation_has_correct_attributes(self):
        settings = S.create()
        annotation_data = {"message": "Teste !!"}
        connection_mock = mock.Mock()
        with patch_with_factory(
            "live_client.connection.autodetect.build_sender_function", connection_mock
        ):
            annotation.create(annotation_data, settings=settings)
            event = connection_mock.call_args[0][0]

            assert event.get("__type") == "__annotations"
            assert bool(event.get("uid")) == True
            assert bool(event["createdAt"]) == True

    def test_raises_if_no_room(self):
        """ Function shall raise if no room"""
        settings = S.create(output={})
        assert raises(KeyError, annotation.create, {}, settings=settings)

    def test_input_params_dont_change(self):
        """ Input params must not change their contents (avoid side effects)"""
        settings = S.create()
        annotation_data = {}
        room = {}
        with patch_with_factory(
            "live_client.connection.autodetect.build_sender_function", no_action
        ):
            _settings = copy.deepcopy(settings)
            _annotation_data = copy.deepcopy(annotation_data)
            _room = copy.deepcopy(room)

            annotation.create(annotation_data, settings, room)

            assert annotation_data == _annotation_data
            assert settings == _settings
            assert room == _room
