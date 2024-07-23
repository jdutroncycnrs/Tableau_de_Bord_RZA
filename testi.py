Liste_Theme = [[132, 'theme'], [166, 'theme'], [194, 'theme'], [210, 'theme']]
Liste_Thesaurus = [[170, 'GEMET'], [198, 'AGROVOC']]
Mots_cles = [
    [114, 'Atmospheric conditions'], [118, 'Environmental monitoring facilities'],
    [122, 'Geology'], [126, 'Meteorological geographical features'], [130, 'Soils'],
    [148, 'atmosphere'], [152, 'karst'], [156, 'geophysics'], [160, 'geodesy'],
    [164, 'hydrogeology'], [180, 'karst'], [184, 'geophysics'], [188, 'geodesy'],
    [192, 'hydrogeology'], [206, 'GEK'], [208, 'SNO H+']
]


def modify_mots_cles(mots_cles, liste_thesaurus, liste_theme):
    modified_list = []
    for mot in mots_cles:
        mot_num = mot[0]
        mot_str = mot[1]
        thesaurus_str = ''
        theme_str = ''
        
        # Find the correct thesaurus string
        for thesaurus in liste_thesaurus:
            if thesaurus[0] < mot_num:
                thesaurus_str = thesaurus[1]
        
        # Find the correct theme string
        for theme in liste_theme:
            if theme[0] < mot_num:
                theme_str = theme[1]
        
        # Append the modified mot with additional elements
        modified_list.append([mot_str, theme_str, thesaurus_str])
    
    return modified_list

# Modify the Mots_cles list
modified_Mots_cles = modify_mots_cles(Mots_cles, Liste_Thesaurus, Liste_Theme)