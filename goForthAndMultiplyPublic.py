import re
import os
from os import listdir
from os.path import isfile, isdir, join

# Path to eu4 installation directory, "...\\steamaps\\common\\Europa Universalis IV"
gameDir = "...\\steamapps\\common\\Europa Universalis IV" #Set this to your EU4 directory, e.g. C:\\...\\steamapps\\common\\Europa Universalis IV
if gameDir == "...\\steamapps\\common\\Europa Universalis IV":
    print("Insert path to your EU4 directory: ")
    gameDir = input()

# Path to the local mod folder, "...\\Documents\\Paradox Interactive\\Europa Universalis IV\\mod\\[Mod Name]"
modDir = "...\\Documents\\Paradox Interactive\\Europa Universalis IV\\mod\\UltimateX10New" #Set this to your local mod folder in "Documents"
if modDir == "...\\Documents\\Paradox Interactive\\Europa Universalis IV\\mod\\UltimateX10New":
    print("Insert path to your local EU4 mod folder: ")
    modDir = input()

commonDir = gameDir + "\\common"
modifiersFile = "modifiers.txt"

# Matches all modifier delcarations
modifierRegex = "([ \t]*(?:.*{.)?(?:[ \t]*\S*[ \t]*=[ \t]*{[ \t]*)*(\S*)[ \t]*=[ \t]*)([0-9-.]+)(.*)"
# Matches if a line is commented out
commentRegex = "^[ \t]*#"

# Tell it to ignore particular folders within common (these directories wouldn't get modified anyway)
ignoreDirs = ["ai_army", "ai_attitudes", "ai_personalities", "bookmarks", "cb_types", "client_states", "colonial_regions", "countries", "country_colors", "country_tags", "cultures", "custom_country_colors", "defines", "diplomatic_actions", "disasters", "dynasty_colors", "estate_agendas", "estates_preload", "governments", "government_names", "imperial_incidents", "incidents", "insults", "natives", "new_diplomatic_actions", "on_actions", "opinion_modifiers", "parliament_bribes", "peace_treaties", "powerprojection", "prices", "province_names", "rebel_types", "region_colors", "religious_conversions", "revolt_triggers", "scripted_effects", "scripted_functions", "scripted_triggers", "subject_types", "timed_modifiers", "tradenodes", "trade_companies", "units", "units_display", "wargoal_types"]
# Tell it to ignore particular modifiers (for "balance" reasons)
ignoreModifiers = ["local_hostile_movement_speed", "hostile_disembark_speed", "local_friendly_movement_speed", "merchants", "fort_level", "brahmins_loyalty_modifier", "rajput_loyalty_modifier", "maratha_loyalty_modifier", "vaisyas_loyalty_modifier", "church_loyalty_modifier", "nobles_loyalty_modifier", "burghers_loyalty_modifier", "cossacks_loyalty_modifier", "nomadic_tribes_loyalty_modifier", "dhimmi_loyalty_modifier", "jains_loyalty_modifier", "all_estate_loyalty_equilibrium", "all_estate_influence_modifier", "brahmins_influence_modifier", "rajput_influence_modifier", "maratha_influence_modifier", "vaisyas_influence_modifier", "church_influence_modifier", "nobles_influence_modifier", "burghers_influence_modifier", "cossacks_influence_modifier", "nomadic_tribes_influence_modifier", "dhimmi_influence_modifier", "jains_influence_modifier", "land_forcelimit", "land_forcelimit_modifier", "special_unit_forcelimit", "naval_forcelimit", "naval_forcelimit_modifier", "vassal_forcelimit_bonus"]
# Tell it to allow particular code blocks used in the static_modifiers directory
allowStaticBlocks = ["BYZ_pronoia_buff_army_tradition_modifier = {", "BYZ_pronoia_land_forcelimit_penalty = {", "BYZ_extra_forcelimit_for_pronoiars = {", "may_dynastic_influence_modifier = {", "soyurghal_base_overlord_modifiers = {", "soyurghal_base_modifiers = {", "culturally_influencing_countries = {", "culturally_influencing_countries_same_culture = {", "culturally_influenced_country = {", "adur_burzhen_mihr_mod = {", "adur_farnbag_mod = {", "adur_gushnasp_mod = {", "mamluks_regiment = {", "qizilbash_regiment = {", "BYZ_discipline = {", "BYZ_army_trad = {", "slackening_modifier = {", "ruler_adm = {", "ruler_dip = {", "ruler_mil = {", "royal_council_meeting_mod = {", "state_council_meeting_mod = {", "war_council_meeting_mod = {", "mobilized_new_order_regiments = {", "cultural_revolution = {", "tercio_regiment = {", "musketeer_regiment = {", "samurai_regiment = {", "geobukseon_ship = {", "man_of_war_ship = {", "galleon_ship = {", "galleass_ship = {", "caravel_ship = {", "voc_indiamen_ship = {", "expansion_focus_modifier = {", "outward_focus_modifier = {", "inward_focus_modifier = {", "equipped_streltsy_modifier_weaker = {", "equipped_streltsy_modifier = {", "karma_just_right = {", "karma_too_high = {", "karma_too_low = {", "overlord_expel_ronin = {", "custom_setup = {", "drilling_armies = {", "tributary_state_behind_overlord_tech_adm = {", "tributary_state_behind_overlord_tech_dip = {", "tributary_state_behind_overlord_tech_mil = {", "fervor = {", "num_of_marriages = {", "gbr_emperor_of_india_subject_bonus = {", "gbr_emperor_of_india_overlord_bonus = {", "militarized_society = {", "difficulty_very_easy_player = {", "difficulty_easy_player = {", "difficulty_hard_ai = {", "difficulty_very_hard_ai = {", "seat_in_parliament = {", "cardinals_spread_institution = {", "patriarch_state = {", "patriarch_authority_local = {", "patriarch_authority_global = {", "pasha_state = {", "march_bonus = {", "pu_subject_bonus = {", "pu_overlord_bonus = {", "devastation = {", "prosperity = {", "war_taxes = {", "privateering = {", "positive_mandate = {", "negative_mandate = {", "lost_mandate_of_heaven = {", "bankruptcy = {", "war = {", "war_exhaustion = {", "doom = {", "authority = {", "mercantilism = {", "army_tradition = {", "navy_tradition = {", "positive_piety = {", "negative_piety = {", "defender_of_faith = {", "defender_of_faith_refused_cta = {", "emperor = {", "states_in_hre = {", "free_cities_in_hre = {", "free_city_in_hre = {", "member_in_hre = {", "curia_controller = {", "bought_indulgence = {", "production_leader = {", "bonus_from_merchant_republics = {", "bonus_from_merchant_republics_for_trade_league_member = {", "merchant_republic_mechanics_modifier = {", "federation_leader = {", "is_great_power = {", "in_golden_era = {", "absolutism = {", "low_army_professionalism = {", "high_army_professionalism = {", "streltsy_modifier = {", "new_world_exploitation_modifier = {", "trade_company_strong = {", "large_colonial_nation = {", "crown_colony_overlord = {", "private_enterprise_overlord = {", "self_governing_colony_overlord = {", "crown_colony_subject = {", "private_enterprise_subject = {", "self_governing_colony_subject = {", "revolution_target = {", "dishonoured_alliance =  {", "recruitment_sabotaged = {", "merchants_slandered = {", "discontent_sowed = {", "reputation_sabotaged = {", "corrupt_officials = {", "scaled_trade_league_leader = {", "in_trade_league = {", "send_officers = {", "karma_just_right =\n{", "karma_too_high =\n{", "karma_too_low =\n{", "invasion_nation = {", "native_policy_coexist = {", "native_policy_trade = {", "native_policy_hostile = {", "high_harmony = {", "low_harmony = {", "overlord_daimyo_at_peace = {", "overlord_daimyo_at_peace_max = {", "overlord_daimyo_at_peace_min = {", "overlord_daimyo_same_isolationism = {", "overlord_daimyo_different_isolationism = {", "overlord_daimyo_isolationism_max = {", "overlord_daimyo_isolationism_min = {", "overlord_sankin_kotai = {", "subject_sankin_kotai = {", "subject_expel_ronin = {", "overlord_sword_hunt = {", "subject_sword_hunt = {", "supply_depot_area = {", "efficient_tax_farming_modifier = {", "land_acquisition_modifier = {", "lenient_taxation_modifier = {", "train_horsemanship_modifier = {", "promote_culture_in_government_modifier = {", "seize_clerical_holdings_modifier = {", "invite_minorities_modifier = {", "hanafi_scholar_modifier = {", "hanbali_scholar_modifier = {", "maliki_scholar_modifier = {", "shafii_scholar_modifier = {", "ismaili_scholar_modifier = {", "jafari_scholar_modifier = {", "zaidi_scholar_modifier = {", "regiment_drill_modifier = {", "army_drill_modifier = {", "janissary_regiment = {", "cawa_regiment = {", "hussars_regiment = {", "marine_regiment = {", "banner_regiment = {", "streltsy_regiment = {", "cossacks_regiment = {", "carolean_regiment = {", "revolutionary_guard_regiment = {", "rajput_regiment = {", "raiding_parties_modifier = {", "serfs_recieved_by_cossacks = {", "cossacks_modifier = {", "expand_administation_modifier = {", "over_governing_capacity_modifier = {", "lost_hegemony = {", "at_peace_revolutionary = {", "expanded_infrastructure = {", "centralize_state = {", "guru_teaching = {", "innovativeness = {", "corruption = {", "inverse_religious_unity = {", "religious_unity = {"]

# I guess diplo rep no longer causes crashes???
# ignoreModifiers += ["diplomatic_reputation"]

# Get all modifiers
fin = open(modifiersFile, "r")
modifiers = []
counters = []
for line in fin:
    if line[:len(line)-1] not in ignoreModifiers:
        modifiers += [line[:len(line)-1]]
        counters += [0]
fin.close()
modifiers += (["base_local_dev_points"])
modifiers += (["local_dev_points_modifier"])
counters += [0, 0]
print(modifiers)
# Some code to skip over modifiers, for testing if a modifier is crashing the game

# skip = [140, 150]
# temp = []
# for i in range(skip[0]):
#     temp += [modifiers[i]]
# for i in range(skip[0], skip[1]):
#     print("\t" + modifiers[i])
# for i in range(skip[1], len(modifiers)):
#     temp += [modifiers[i]]
# modifiers = temp

# Finds all modifier declarations in all files in a directory and rewrites those files to the mod directory with the value multiplied by 10
def reWrite(directory):
    counter = 0
    unusedDir = True
    for file in [f for f in listdir(gameDir + directory) if isfile(join(gameDir + directory, f))]:
        print("\t" + file)
        skipBlock = 0
        unusedFile = True
        fin = open(gameDir + directory + file, "r", encoding="Latin-1")
        fileText = ""
        skipStaticBlock = False
        for line in fin:
            match = re.search(modifierRegex, line)

            # ignore ai code blocks and conditional code blocks
            if(file != "00_static_modifiers.txt"):
                if line[0] != '#' and ( line.find("ai_will_do = {") != -1 or line.find("trigger = {") != -1 or line.find("allow = {") != -1 or line.find("target_province_weights = {") != -1 or line.find("chance = {") != -1 or line.find("can_select = {") != -1 or line.find("ai = {") != -1):
                    skipBlock += 1
                elif skipBlock != 0 and line.find("{") != -1:
                    skipBlock += 1
                elif skipBlock == 0 and line.find("if = {") != -1:
                    skipBlock += 1
                if skipBlock != 0 and line.find("}") != -1:
                    skipBlock -= 1
            else:
                if not line[0].isspace() and line[0] != '#':
                    skipStaticBlock = True
                    for blockName in allowStaticBlocks:
                        if(line.find(blockName) != -1):
                            skipStaticBlock = False
                            break

            # if not skipping current block, find modifiers in current line and modify its value by 10
            if skipBlock == 0 and skipStaticBlock == False and re.search(commentRegex, line) == None and match != None and (file != "05_government_reforms_natives.txt" or match.group(2) != "reform_progress_growth") and match.group(2) in modifiers:
                unusedDir = False
                unusedFile = False
                counter += 1
                counters[modifiers.index(match.group(2))] += 1
                multiplier = 10

                modifier = match.group(2)
                number = match.group(3)
                if file == "00_buildings.txt":
                    print(modifier)
                # if current modifier is election_cycle, multiply by 1.5       
                # else if current file is for military tech, or if modifier is for base development cost, diplomatic relations, or diplomats, multiply modifiers by 2
                if modifier == "election_cycle":
                    multiplier = 1.5
                elif file == "mil.txt" or modifier == "development_cost_modifier" or modifier == "local_development_cost_modifier" or modifier == "diplomatic_upkeep" or modifier == "diplomats":
                    multiplier = 2

                if modifier == "reinforce_speed" and float(number) < -0.09:
                    fileText += match.group(1) + "-0.90" + match.group(4) + "\t\t# Set to -90%, originally " + number + "\n"
                else:
                    fileText += match.group(1) + str(round(float(number) * multiplier, 3)) + match.group(4) + "\t\t# Multiplied by " + str(multiplier) + "\n"
            else:
                fileText += line
        if unusedFile == False:
            fout = open(modDir + directory + file, "w+", encoding="Latin-1")
            fout.write(fileText)
            fout.close()
        fin.close()
    if unusedDir == True:   # alert if a directory is left unmodified
        print("*** UNUSED: " + directory + "***")
    return counter

counter = 0
# All files in all directories in common excluding ignoreDirs directories
if not os.path.exists(modDir + "\\common"):
    os.makedirs(modDir + "\\common")

for directory in [dir for dir in [d for d in listdir(commonDir) if isdir(join(commonDir, d))] if dir not in ignoreDirs]:
    print(directory)
    if not os.path.exists(modDir + "\\common\\" + directory):
        os.makedirs(modDir + "\\common\\" + directory)
    counter += reWrite("\\common\\" + directory + "\\")

print(str(counter) + " lines have been modified")
print(modifiers[counters.index(max(counters))] + " was modified the most at " + str(max(counters)) + " times")

# I believe these will only make triggers for decisions, events, and missions x10 (making many impossible)

# # All files in decisions
# print("decisions")
# if not os.path.exists(modDir + "\\decisions"):
#     os.makedirs(modDir + "\\decisions")
# reWrite("\\decisions\\")

# # All files in events
# print("events")
# if not os.path.exists(modDir + "\\events"):
#     os.makedirs(modDir + "\\events")
# reWrite("\\events\\")

# # All files in missions
# print("missions")
# if not os.path.exists(modDir + "\\missions"):
#     os.makedirs(modDir + "\\missions")
# reWrite("\\missions\\")
