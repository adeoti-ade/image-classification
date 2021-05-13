from rest_framework import serializers

valid_mobile_prefix = ["701", "702" "0703", "0704", "0706", "707", "708",
                       "801", "802", "803", "806", "807", "808", "809",
                       "810", "811", "812", "813", "814", "815", "816", "817", "818", "819",
                       "901", "902", "903", "904", "905", "906", "907", "908", "909"]


def is_valid_mobile(value):
    # if len(value) != 11 or value != 13:
    #     raise serializers.ValidationError(detail={"mobile": "mobile must be 11 or 13"})

    if len(value) == 11:
        first_three_digits = value[1:3]
        if first_three_digits not in valid_mobile_prefix:
            raise serializers.ValidationError(
                detail={"mobile": "mobile must be one of {}".format(",".join(valid_mobile_prefix))})

        return value
    elif len(value) == 13:
        if not value.startswith("234"):
            raise serializers.ValidationError(
                detail={"mobile": "mobile must be one of starts with 234"})
        first_three_digits = value[3:6]
        if first_three_digits not in valid_mobile_prefix:
            raise serializers.ValidationError(
                detail={"mobile": "mobile must be one of {}".format(",".join(valid_mobile_prefix))})

        return value
    raise serializers.ValidationError(
        detail={"mobile": "invalid mobile number"})
