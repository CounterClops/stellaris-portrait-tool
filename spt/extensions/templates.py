class Portraits:
    def __init__(self, portrait_group_name:str="mod_portrait_group", portrait_refs:list=[], portrait_files:dict={"texturefile": ""}):
        self.config = {
            "portraits": portrait_files,
            "portrait_groups": {
                portrait_group_name: {
                    "default": portrait_refs[0],
                    "game_setup": {
                        "add": {
                            "portraits": portrait_refs
                        }
                    },
                    "species": {
                        "add": {
                            "portraits": portrait_refs
                        }
                    },
                    "pop" : {
                        "add": {
                            "portraits": portrait_refs
                        }
                    },
                    "leader": {
                        "add": {
                            "portraits": portrait_refs
                        }
                    },
                    "ruler": {
                        "add": {
                            "portraits": portrait_refs
                        }
                    }
                }
            }
        }

class PortraitSets:
    def __init__(self, portrait_set_name:str="mod_portrait_set", species_class_name:str="mod_species_class", portraits:dict=[]):
        self.config = {
            portrait_set_name: {
                "species_class": species_class_name,
                "portraits": portraits
            }
        }

class SpeciesClass:
    def __init__(self, species_class_name:str="mod_species_class", portraits:list=[], archetype:str="BIOLOGICAL"):
        if archetype == "BIOLOGICAL":
            self.config = {
                species_class_name: {
                    "archetype" : "BIOLOGICAL",
                    "possible": {
                        "authority": {
                            "NOT": {
                                "value": "auth_machine_intelligence",
                                "text": "SPECIES_CLASS_MUST_NOT_USE_MACHINE_INTELLIGENCE"
                            }
                        }
                    },
                    "custom_portraits": {
                        "trigger":  {
                            "always": "yes"
                        },
                        "portraits": portraits # Should list the portrait groups attached to this Species Class
                    },
                    "graphical_culture": "mammalian_01",
                    "move_pop_sound_effect": "moving_pop_confirmation",
                    "resources": {}
                }
            }
        else:
            pass

class SpeciesNames:
    machine_config = {
        "name": "Machine",
        "plural": "Machines",
        "home_planet": "CPU",
        "home_system": "Motherboard",
        "name_list": "MACHINE4"
    }

class PortraitCategories:
    def __init__(self, category_name:str="", portrait_sets:list=[]):
        self.config = {
            category_name: {
                "name": category_name,
                "sets": [
                    portrait_sets
                ]
            }
        }