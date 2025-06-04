# Module adafruit-2348 

A Viam module for controlling the Adafruit DC Motor HAT (2348) with up to 4 DC motors.

## Model ianwhalen-viam:adafruit-2348:adafruit-2348

This model provides control for DC motors connected to an Adafruit Motor HAT (2348). It supports up to 4 motors and provides basic motor control functionality.

### Configuration
The following attribute template must be used to configure this model:

```json
{
  "motor_index": <integer>
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `motor_index` | integer | Required  | The index of the motor to control (0-3). 0 corresponds to motor1, 1 to motor2, etc. |

#### Example Configuration

```json
{
  "motor_index": 0
}
```

### Supported Operations

The motor supports the following operations:
- `set_power`: Set the motor power (-1.0 to 1.0)
- `stop`: Stop the motor
- `is_powered`: Check if the motor is powered and get current power level
- `is_moving`: Check if the motor is currently moving

Note: Some operations like `go_for`, `go_to`, `set_rpm`, `reset_zero_position`, `get_position`, and `get_properties` are not implemented in this version.
