# `class Rate`

`classes.rate.Rate(parent=None, func=None, min_vel=None, max_vel=None, a=None, b=None, c=None, d=None)`

Rate object contain the information of the efficiency curve. This efficiency is represented by 4 parameters a,b,c, d and a function which can be either a double tangeate form called "tan", either an exponential form, called "square".

"tan" form:

$$
f(m) = \frac{a}{4} * \left[1-tanh\left(\frac{m-b}{c}\right)\right] * \left[1-tanh\left(\frac{m-b}{d}\right)\right]
$$

"square" form:

$$
f(m) = \frac{a-b*(m-21)^2}{1+\exp\left(\frac{m-c}{d}\right)}
$$

**Parameters**

See object attributes below.

## Class attributes

### `all : list`
List containing all instaces of the class, which allow to easily iterate over them.

---

## Class methods

No methods in this class

---

## Object attributes

### `parent : Block | Triplet`
Object associated to this rate. It ccan be either a Block or a Triplet

### `func : str`
Name of the function used ("tan" or "square")

### `min_vel : float`
Minimum velocity taken in account in this rate of detection.

### `max_vel : float`
Maximum velocity taken in account in this rate of detection.

### `a : float`
Function parameter (see formula above)

### `b : float`
Function parameter (see formula above)

### `c : float`
Function parameter (see formula above)

### `d : float`
Function parameter (see formula above)

---

## Object methods

### points

`points(mag = linspace(21, 26, 1000, endpoint=True))`

Return an array containing the value of the efficiency curve according to the range of magnitude given in parameter.

**Parameters**
- `mag : ndarray` magnitudes for which the function will be evaluated. By default, mag contain 1000 equally distant points in a range of magnitude contained between 21 and 26. 

### to_disct

`to_dict()`

Return a dictionary containing all the object information. Useful to save it in a JSON format.

**Parameters**: None

**Returns**:

- `dict`: The containing all the object information.

### to_ai_ready

`to_ai_ready(as_points = False, **kwargs)`

Return a vector that can be used to train the AI.

**Parameters**:

- `mag : ndarray | None` : if `None` (default behavior), the function will return an array containing the parameters of the efficiency model. If this parameter is set, the function will return the value of the efficiency for each `mag` value.
- `**krags` this parameter is not used. It only allow to quicly adapt a code that contain call to this function on upper classes without having to edit all the parameters.

**Returns**:

- `ndarray`: A Numpy vector containing the parameters