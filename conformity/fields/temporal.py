import datetime
from typing import (
    Any as AnyType,
    Generic,
    TypeVar,
)

from conformity.fields.base import BaseField
from conformity.fields.utils import strip_none
from conformity.types import (
    Error,
    Validation,
)
from conformity.typing import Introspection


try:
    # noinspection PyUnresolvedReferences
    from freezegun import api as _freeze
    DATETIME_TYPES = (datetime.datetime, _freeze.FakeDatetime)
    DATE_TYPES = (datetime.date, _freeze.FakeDate)
except ImportError:
    DATETIME_TYPES = datetime.datetime
    DATE_TYPES = datetime.date


T = TypeVar('T', datetime.date, datetime.time, datetime.datetime, datetime.timedelta)


class TemporalBase(Generic[T], BaseField):
    """
    Common base class for all temporal types. Cannot be used on its own without extension.
    """

    # These three must be overridden
    valid_type = None
    valid_noun = None
    introspect_type = None

    def __init__(
        self,
        *,
        gt: T=None,
        gte: T=None,
        lt: T=None,
        lte: T=None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.gt = self.validate_parameter('gt', gt)
        self.gte = self.validate_parameter('gte', gte)
        self.lt = self.validate_parameter('lt', lt)
        self.lte = self.validate_parameter('lte', lte)

    @classmethod
    def validate_parameter(cls, name: str, value: T) -> T:
        if value is not None and not isinstance(value, self.valid_type):
            raise TypeError((
                "'{}' value {!r} cannot be used for "
                "comparisons in this type"
            ).format(name, value))
        return value

    def validate(self, value: AnyType) -> Validation:
        v = super().validate(value)
        if v.errors:
            return v

        errors = []
        if self.gt is not None and value <= self.gt:
            errors.append(Error('Value not > {}'.format(self.gt)))
        if self.gte is not None and value < self.gte:
            errors.append(Error('Value not >= {}'.format(self.gte)))
        if self.lt is not None and value >= self.lt:
            errors.append(Error('Value not < {}'.format(self.lt)))
        elif self.lte is not None and value > self.lte:
            errors.append(Error('Value not <= {}'.format(self.lte)))
        return Validation(errors=errors)

    def introspect(self) -> Introspection:
        return strip_none({
            'gt': str(self.gt) if self.gt else None,
            'gte': str(self.gte) if self.gte else None,
            'lt': str(self.lt) if self.lt else None,
            'lte': str(self.lte) if self.lte else None,
        }).update(super().introspect())


class DateTime(TemporalBase[DATETIME_TYPES])
    """
    Validates that the value is a `datetime.datetime` instance and optionally
    enforces boundaries for that `datetime` with the `gt`, `gte`, `lt`, and
    `lte` arguments, which must also be `datetime` instances if specified.
    """

    valid_type = DATETIME_TYPES
    valid_noun = 'a datetime.datetime'
    introspect_type = 'datetime'


class Date(TemporalBase[DATE_TYPES]):
    """
    Validates that the value is a `datetime.date` instance and optionally
    enforces boundaries for that `date` with the `gt`, `gte`, `lt`, and `lte`
    arguments, which must also be `date` instances if specified.
    """

    valid_type = DATE_TYPES
    valid_noun = 'a datetime.date'
    introspect_type = 'date'


class Time(TemporalBase[datetime.time]):
    """
    Validates that the value is a `datetime.time` instance and optionally
    enforces boundaries for that `time` with the `gt`, `gte`, `lt`, and `lte`
    arguments, which must also be `time` instances if specified.
    """

    valid_type = datetime.time
    valid_noun = 'a datetime.time'
    introspect_type = 'time'


class TimeDelta(TemporalBase[datetime.timedelta]):
    """
    Validates that the value is a `datetime.timedelta` instance and optionally
    enforces boundaries for that `timedelta` with the `gt`, `gte`, `lt`, and
    `lte` arguments, which must also be `timedelta` instances if specified.
    """

    valid_type = datetime.timedelta
    valid_noun = 'a datetime.timedelta'
    introspect_type = 'timedelta'


class TZInfo(BaseField):
    """
    Validates that the value is a `datetime.tzinfo` instance.
    """

    valid_type = datetime.tzinfo
    valid_noun = 'a datetime.tzinfo'
    introspect_type = 'tzinfo'
