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
    def __init__(self, portrait_set_name:str="mod_portrait_set", species_class_name:str="mod_species_class", portraits:list=[]):
        self.config = {
            portrait_set_name: {
                "species_class": species_class_name,
                "portraits": portraits
            }
        }

class SpeciesClass:
    def __init__(self, species_class_name:str="mod_species_class", archetype:str="BIOLOGICAL"):
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
                        }
                    },
                    "graphical_culture": "mammalian_01",
                    "move_pop_sound_effect": "moving_pop_confirmation",
                    "resources": {}
                }
            }
        elif archetype == "MACHINE":
            self.config = {
                species_class_name: {
                    "archetype": "MACHINE",
                    "possible": {
                        "OR": {
                            "AND": {
                                "host_has_dlc": "The Machine Age",
                                "authority": {
                                    "NOT": {
                                        "value": "auth_hive_mind"
                                    }
                                }
                            },
                            "authority": {
                                "OR": { 
                                    "value": "auth_machine_intelligence",
                                    "text": "SPECIES_CLASS_MUST_USE_MACHINE_INTELLIGENCE"
                                }
                            }
                        }
                    },
                    "possible_secondary": {
                        "OR": {
                            "AND": {
                                "host_has_dlc": "The Machine Age",
                                "civics": {
                                    "NOT": {
                                        "value": "civic_machine_servitor"
                                    }
                                }
                            },
                            "OR": {
                                "always": "no",
                                "text": "SECONDARY_SPECIES_CLASS_INVALID"
                            }
                        }
                    },
                    "playable": {
                        "OR": {
                            "host_has_dlc": "Synthetic Dawn Story Pack",
                            "has_machine_age_dlc": "yes"
                        }
                    },
                    "randomized": {
                        "OR": {
                            "host_has_dlc": "Synthetic Dawn Story Pack",
                            "has_machine_age_dlc": "yes"
                        },
                        # The create_species effect can't properly take the possible trigger below into account.
                        # Work around this by disabling this class for species randomization after game start.
                        "NOT": {
                            "has_global_flag": "game_started"
                        }
                    },

                    "trait": "trait_machine_unit",
                    "gender": "yes",
                    "use_climate_preference": "no",
                    "portrait_modding": "yes",

                    "leader_age_min": 5,
                    "leader_age_max": 10,

                    "graphical_culture": "synthetics_01",
                    "move_pop_sound_effect": "robot_pops_move",
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