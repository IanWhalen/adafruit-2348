from dataclasses import dataclass
from typing import (Any, ClassVar, Dict, List, Mapping, Optional,
                    Sequence, Tuple)

from typing_extensions import Self
from viam.components.motor import *
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes, struct_to_dict
from adafruit_motorkit import MotorKit
from adafruit_motor.motor import DCMotor


class Adafruit2348(Motor, EasyResource):
    # To enable debug-level logging, either run viam-server with the --debug option,
    # or configure your resource/machine to display debug logs.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("ianwhalen-viam", "adafruit-2348"), "adafruit-2348"
    )

    def __init__(self, name: str):
        super().__init__(name)
        try:
            # Initialize the MotorKit
            self.logger.info("Initializing MotorKit...")
            self._kit = MotorKit()
            self.logger.info("MotorKit initialized successfully")
            
            # Get the motor objects
            self._motors = [
                self._kit.motor1,
                self._kit.motor2,
                self._kit.motor3,
                self._kit.motor4,
            ]
            self.logger.info("Motor objects created successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize MotorKit: {str(e)}")
            raise RuntimeError(f"Failed to initialize MotorKit: {str(e)}")
            
        # Track power state and movement state for each motor
        self._power_states: dict[int, float] = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}  # motor index -> power level
        self._is_moving: dict[int, bool] = {0: False, 1: False, 2: False, 3: False}  # motor index -> is moving

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Motor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both required and optional)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> tuple[Sequence[str], Sequence[str]]:
        """Validate the configuration object and return required and optional dependencies.

        Returns:
            tuple[Sequence[str], Sequence[str]]: (required_dependencies, optional_dependencies)
        """
        if "motor_index" not in config.attributes.fields:
            raise Exception("motor_index must be specified in the configuration and be an integer between 0 and 3 (inclusive).")
        motor_index = config.attributes.fields["motor_index"]

        if not motor_index.HasField("number_value"):
            raise Exception("motor_index must be anumber value.")
        motor_index_value = motor_index.number_value
        
        if not (motor_index_value == int(motor_index_value)):
            raise Exception("motor_index must be an integer.")
        
        if motor_index_value < 0 or motor_index_value > 3:
            raise Exception("motor_index must be between 0 and 3 (inclusive).")
        
        return [], []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both required and optional)
        """
        attrs = struct_to_dict(config.attributes)
        self._motor_index = int(attrs["motor_index"])
        self.logger.info(f"Using motor {self._motor_index}")
        
        return super().reconfigure(config, dependencies)

    @dataclass
    class Properties(Motor.Properties):
        supports_position_control: bool
        supports_power_control: bool
        supports_brake: bool
        supports_revolutions_counted: bool
        position_reporting: bool

    async def set_power(
        self,
        power: float,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        """Set the power of the motor.
        
        Args:
            power (float): Power between -1.0 and 1.0
                - Negative values make the motor spin backwards
                - Positive values make the motor spin forwards
                - 0.0 stops the motor
        """
        # Use the configured motor index
        motor_index = self._motor_index
        
        # Clamp power between -1.0 and 1.0
        power = max(min(power, 1.0), -1.0)
        
        # Update internal state
        self._power_states[motor_index] = power
        self._is_moving[motor_index] = power != 0.0
        
        # Log the power level
        self.logger.info(f"Setting motor {motor_index} power to {power}")
        
        # Get the motor object
        motor: DCMotor = self._motors[motor_index]
        
        # Set the motor direction and throttle together
        if power == 0:
            motor.throttle = 0
        else:
            motor.throttle = power

    async def go_for(
        self,
        rpm: float,
        revolutions: float,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.error("`go_for` is not implemented")
        raise NotImplementedError()

    async def go_to(
        self,
        rpm: float,
        position_revolutions: float,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.error("`go_to` is not implemented")
        raise NotImplementedError()

    async def set_rpm(
        self,
        rpm: float,
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.error("`set_rpm` is not implemented")
        raise NotImplementedError()

    async def reset_zero_position(
        self,
        offset: float,
        *,
        extra: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        self.logger.error("`reset_zero_position` is not implemented")
        raise NotImplementedError()

    async def get_position(
        self,
        *,
        extra: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> float:
        self.logger.error("`get_position` is not implemented")
        raise NotImplementedError()

    async def get_properties(
        self,
        *,
        extra: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Properties:
        return self.Properties(
            supports_position_control=False,
            supports_power_control=True,
            supports_brake=False,
            supports_revolutions_counted=False,
            position_reporting=False,
        )

    async def stop(
        self,
        *,
        extra: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ):
        """Stop the motor."""
        self.logger.info("Stop command received")
        # Use the configured motor index
        motor_index = self._motor_index
        # Update internal state
        self._power_states[motor_index] = 0.0
        self._is_moving[motor_index] = False
        # Actually stop the motor
        motor = self._motors[motor_index]
        motor.throttle = 0.0  # This will stop the motor

    async def is_powered(
        self,
        *,
        extra: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> tuple[bool, float]:
        """Return whether the motor is powered and the current power level.
        Returns:
            Tuple[bool, float]: A tuple containing:
                - bool: Whether the motor is powered
                - float: The current power level (-1.0 to 1.0)
        """
        # Use the configured motor index
        motor_index = self._motor_index
        power = self._power_states[motor_index]
        return abs(power) > 0.0, power

    async def is_moving(self) -> bool:
        """Return whether the motor is currently moving.
        Returns:
            bool: True if the motor is moving, False otherwise
        """
        # For now, we'll assume motor 0 is the one being queried
        # In a real implementation, you'd want to get the motor index from extra
        motor_index = 0
        return self._is_moving[motor_index]

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        self.logger.error("`do_command` is not implemented")
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> list[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()
