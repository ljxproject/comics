from rest_framework import serializers

from userapi.models import Permission, User
from userapi.models.feedback import FeedBackDetail, FeedBack


class ComicsSuccessSerializer(serializers.BaseSerializer):
    def to_representation(self, data):
        return {
            "code": "200",
            "msg": "OK",
            "data": data
        }


class UsersGenderSerializer(serializers.Serializer):
    gender = serializers.CharField(max_length=1)
    email = serializers.CharField(max_length=64)

    # class Meta:
    #     model = User
    #     fields = ("gender", "email")


class UsersEmailSerializer(serializers.Serializer):
    newName = serializers.CharField(max_length=64)
    oldNmail = serializers.CharField(max_length=64)
    pin = serializers.CharField(max_length=6)
    # class Meta:
    #     model = User
    #     fields = ("pin", "newEmail", "oldEmail")


class UsersNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)
    email = serializers.CharField(max_length=64)
    # class Meta:
    #     model = User
    #     fields = ("name", "email")


class UsersWalletSerializer(serializers.Serializer):
    txID = serializers.CharField(max_length=25)
    # class Meta:
    #     model = User
    #     fields = ("wallet", "email")


class CreateOderSerializer(serializers.Serializer):
    gmv = serializers.CharField(max_length=10)
    email = serializers.CharField(max_length=64)
    platform = serializers.CharField(max_length=10)


class UsersAvaterSerializer(serializers.Serializer):
    avatar = serializers.ImageField()
    email = serializers.CharField(max_length=64)

    # class Meta:
    #     model = User
    #     fields = ("avatar", "email")


class PurchaseChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('email', 'com_id', 'chap_id')


class FeedBackDetailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=64, required=True,
                                   error_messages={"blank": "This field may not be blank.",
                                                   "invalid": "Enter a valid email address."},
                                   help_text="Enter Manga Burger email account.",
                                   style={'placeholder': "required"}
                                   )
    title = serializers.CharField(max_length=100, required=True,
                                  help_text="Enter feedback title.",
                                  error_messages={"blank": "This field may not be blank.",
                                                  "invalid": "This field not more than 100 character."},
                                  style={'autofocus': True, 'placeholder': "required"})
    system = serializers.CharField(max_length=16, allow_blank=True,
                                   help_text="Enter your system version. (ios or android)",
                                   error_messages={"invalid": "This field not more than 16 character."}
                                   )
    content = serializers.CharField(required=True,
                                    help_text="Enter feedback content.",
                                    error_messages={"blank": "This field may not be blank."},
                                    style={'placeholder': "required", 'base_template': 'textarea.html'},
                                    )
    picture = serializers.ImageField(allow_empty_file=True,
                                     allow_null=True,
                                     help_text="Enter feedback screenshot.",
                                     error_messages={'invalid_image': "Upload a valid image. \
                                                                      The file you uploaded was \
                                                                      either not an image or a corrupted image."
                                                     }
                                     )

    def validate_email(self, email):
        if not User.filter(email=email):
            raise serializers.ValidationError("Please enter Manga Burger email account.")
        return email


class FeedBackAwardSerializer(serializers.Serializer):
    award = serializers.IntegerField(required=True, label="奖励金额",
                                     help_text="奖励金额为:[$0-$10]",
                                     style={'autofocus': True})

    def validate_award(self, award):
        if award > 10 or award < 0:
            raise serializers.ValidationError("奖励金额为:[$0-$10]")
        return award
