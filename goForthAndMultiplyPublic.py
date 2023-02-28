import re
import os
from os import listdir
from os.path import isfile, isdir, join

# Path to eu4 installation directory, "...\\steamaps\\common\\Europa Universalis IV"
gameDir = "D:\\Stim\\steamapps\\common\\Europa Universalis IV"
# Path to the local mod folder "...\\Documents\\Paradox Interactive\\Europa Universalis IV\\mod\\[Mod Name]"
modDir = "C:\\Users\\Ryan Cavasso\\Documents\\Paradox Interactive\\Europa Universalis IV\\mod\\UltimateX10Test"
commonDir = gameDir + "\\common"
modifiersFile = "modifiers.txt"

# Matches all modifier delcarations (also matches a bunch of other stuff)
modifierRegex = "((?:[ \t]*\S*[ \t]*=[ \t]*{[ \t]*)*)(\S*)[ \t]*=[ \t]*([0-9-.]+)(.*)"
# Matches if a line is commented out
commentRegex = "^[ \t]*#"

# Tell it to ignore particular folders within common (these directories wouldn't get modified anyway)
ignoreDirs = ["ai_army", "ai_attitudes", "ai_personalities", "bookmarks", "cb_types", "client_states", "colonial_regions", "countries", "country_colors", "country_tags", "cultures", "custom_country_colors", "defines", "diplomatic_actions", "disasters", "dynasty_colors", "estate_agendas", "estates_preload", "governments", "government_names", "imperial_incidents", "incidents", "insults", "natives", "new_diplomatic_actions", "on_actions", "opinion_modifiers", "parliament_bribes", "peace_treaties", "powerprojection", "prices", "province_names", "rebel_types", "region_colors", "religious_conversions", "revolt_triggers", "scripted_effects", "scripted_functions", "scripted_triggers", "subject_types", "timed_modifiers", "tradenodes", "trade_companies", "units", "units_display", "wargoal_types"]
# Tell it to ignore particular modifiers (for "balance" reasons)
ignoreModifiers = ["local_hostile_movement_speed", "hostile_disembark_speed", "local_friendly_movement_speed", "diplomats", "merchants", "fort_level", "brahmins_loyalty_modifier", "rajput_loyalty_modifier", "maratha_loyalty_modifier", "vaisyas_loyalty_modifier", "church_loyalty_modifier", "nobles_loyalty_modifier", "burghers_loyalty_modifier", "cossacks_loyalty_modifier", "nomadic_tribes_loyalty_modifier", "dhimmi_loyalty_modifier", "jains_loyalty_modifier", "all_estate_loyalty_equilibrium", "all_estate_influence_modifier", "brahmins_influence_modifier", "rajput_influence_modifier", "maratha_influence_modifier", "vaisyas_influence_modifier", "church_influence_modifier", "nobles_influence_modifier", "burghers_influence_modifier", "cossacks_influence_modifier", "nomadic_tribes_influence_modifier", "dhimmi_influence_modifier", "jains_influence_modifier", "land_forcelimit", "land_forcelimit_modifier", "special_unit_forcelimit", "naval_forcelimit", "naval_forcelimit_modifier", "vassal_forcelimit_bonus"]
# Tell it to allow particular code blocks used in the static_modifiers directory
allowStaticBlocks = ["militarized_society = {", "difficulty_very_easy_player = {", "difficulty_easy_player = {", "difficulty_hard_ai = {", "difficulty_very_hard_ai = {", "seat_in_parliament = {", "cardinals_spread_institution = {", "patriarch_state = {", "patriarch_authority_local = {", "patriarch_authority_global = {", "pasha_state = {", "march_bonus = {", "pu_subject_bonus = {", "pu_overlord_bonus = {", "devastation = {", "prosperity = {", "war_taxes = {", "privateering = {", "positive_mandate = {", "negative_mandate = {", "lost_mandate_of_heaven = {", "bankruptcy = {", "war = {", "war_exhaustion = {", "doom = {", "authority = {", "mercantilism = {", "army_tradition = {", "navy_tradition = {", "positive_piety = {", "negative_piety = {", "defender_of_faith = {", "defender_of_faith_refused_cta = {", "emperor = {", "states_in_hre = {", "free_cities_in_hre = {", "free_city_in_hre = {", "member_in_hre = {", "curia_controller = {", "bought_indulgence = {", "production_leader = {", "bonus_from_merchant_republics = {", "bonus_from_merchant_republics_for_trade_league_member = {", "merchant_republic_mechanics_modifier = {", "federation_leader = {", "is_great_power = {", "in_golden_era = {", "absolutism = {", "low_army_professionalism = {", "high_army_professionalism = {", "streltsy_modifier = {", "new_world_exploitation_modifier = {", "trade_company_strong = {", "large_colonial_nation = {", "crown_colony_overlord = {", "private_enterprise_overlord = {", "self_governing_colony_overlord = {", "crown_colony_subject = {", "private_enterprise_subject = {", "self_governing_colony_subject = {", "revolution_target = {", "dishonoured_alliance =  {", "recruitment_sabotaged = {", "merchants_slandered = {", "discontent_sowed = {", "reputation_sabotaged = {", "corrupt_officials = {", "scaled_trade_league_leader = {", "in_trade_league = {", "send_officers = {", "karma_just_right =\n{", "karma_too_high =\n{", "karma_too_low =\n{", "invasion_nation = {", "native_policy_coexist = {", "native_policy_trade = {", "native_policy_hostile = {", "high_harmony = {", "low_harmony = {", "overlord_daimyo_at_peace = {", "overlord_daimyo_at_peace_max = {", "overlord_daimyo_at_peace_min = {", "overlord_daimyo_same_isolationism = {", "overlord_daimyo_different_isolationism = {", "overlord_daimyo_isolationism_max = {", "overlord_daimyo_isolationism_min = {", "overlord_sankin_kotai = {", "subject_sankin_kotai = {", "subject_expel_ronin = {", "overlord_sword_hunt = {", "subject_sword_hunt = {", "supply_depot_area = {", "efficient_tax_farming_modifier = {", "land_acquisition_modifier = {", "lenient_taxation_modifier = {", "train_horsemanship_modifier = {", "promote_culture_in_government_modifier = {", "seize_clerical_holdings_modifier = {", "invite_minorities_modifier = {", "hanafi_scholar_modifier = {", "hanbali_scholar_modifier = {", "maliki_scholar_modifier = {", "shafii_scholar_modifier = {", "ismaili_scholar_modifier = {", "jafari_scholar_modifier = {", "zaidi_scholar_modifier = {", "regiment_drill_modifier = {", "army_drill_modifier = {", "janissary_regiment = {", "cawa_regiment = {", "hussars_regiment = {", "marine_regiment = {", "banner_regiment = {", "streltsy_regiment = {", "cossacks_regiment = {", "carolean_regiment = {", "revolutionary_guard_regiment = {", "rajput_regiment = {", "raiding_parties_modifier = {", "serfs_recieved_by_cossacks = {", "cossacks_modifier = {", "expand_administation_modifier = {", "over_governing_capacity_modifier = {", "lost_hegemony = {", "at_peace_revolutionary = {", "expanded_infrastructure = {", "centralize_state = {", "guru_teaching = {", "innovativeness = {", "corruption = {", "inverse_religious_unity = {", "religious_unity = {"]

# Tell it to ignore diplomatic reputation (High diplomatic reputation seems to consistently crash the game so keep this on)
ignoreModifiers += ["diplomatic_reputation"]

# Get all modifiers
fin = open(modifiersFile, "r")
modifiers = []
counters = []
for line in fin:
    if line[:len(line)-1] not in ignoreModifiers:
        modifiers += [line[:len(line)-1]]
        counters += [0]
fin.close()

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
    bad = True
    for file in [f for f in listdir(gameDir + directory) if isfile(join(gameDir + directory, f))]:
        # print("\t" + file)
        skipBlock = 0
        unused = True
        fin = open(gameDir + directory + file, "r", encoding="Latin-1")
        fileText = ""
        skipStaticBlock = False
        for line in fin:
            match = re.search(modifierRegex, line)

            # ignore ai_will_do, trigger, allow, target_province_weights, and if code blocks (and a bunch of others lol)
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
                if not line[0].isspace():
                    skipStaticBlock = True
                    for blockName in allowStaticBlocks:
                        if(line.find(blockName) != -1):
                            skipStaticBlock = False
                            break
                

            if skipBlock == 0 and skipStaticBlock == False and re.search(commentRegex, line) == None and match != None and match.group(2) in modifiers:
                bad = False
                unused = False
                counter += 1
                counters[modifiers.index(match.group(2))] += 1
                if match.group(2) == "election_cycle":
                    fileText += match.group(1) + match.group(2) + " = " + str(round(float(match.group(3)) *  1.5, 2)) + match.group(4) + "\n"
                elif file == "mil.txt":
                    fileText += match.group(1) + match.group(2) + " = " + str(round(float(match.group(3)) *  2, 2)) + match.group(4) + "\n"
                else:
                    fileText += match.group(1) + match.group(2) + " = " + str(round(float(match.group(3)) * 10, 2)) + match.group(4) + "\n"
            else:
                fileText += line
        if unused == False:
            fout = open(modDir + directory + file, "w+", encoding="Latin-1")
            fout.write(fileText)
            fout.close()
        fin.close()
    if bad == True:
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
