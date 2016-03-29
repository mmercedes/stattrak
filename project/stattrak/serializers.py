from rest_framework import serializers

class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ('teamSize', 'name', 'logo')

        def create(self, validated_data):
            league = League()
            league.teamSize = validated_data.get('teamSize', instance.teamSize)
            league.name = validated_data.get('name', instance.name)
            league.logo = validated_data.get('logo', instance.logo)
            league.save()
            return league

        def update(self, instance, validated_data):
            instance.teamSize = validated_data.get('teamSize', instance.teamSize)
            instance.name = validated_data.get('name', instance.name)
            instance.logo = validated_data.get('logo', instance.logo)
            instance.save()
            return instance
        
