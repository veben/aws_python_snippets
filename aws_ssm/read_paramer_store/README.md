# List AWS SSM

> With Pycharm, mark `read_parameter_store` as **Sources Root**

## I. Required setting
If not already done, follow [requirements](../../requirements.md) guide

## II. Launch unit tests
```sh
python -m unittest
```

## III. Launch programs
A parameter named `/config/db/url` need to be created in **AWS Parameter store**
It need to be typed as *SecuredString*

```sh
python read_parameter_store.py
```