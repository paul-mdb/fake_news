def remove_useless(paragraph_ann):
    content = paragraph_ann["content"]
    paragraphs_to_delete = []
    entities_to_delete = []

    for index, paragraph in enumerate(content) :
        if 'label' in paragraph.keys() and paragraph["label"]==0:
            paragraphs_to_delete.append(index)

        else :
            if type(paragraph["content"])==list:
              for index_entity, entity_content in enumerate(paragraph["content"]):
                if type(entity_content) == dict and 'label' in entity_content.keys() and entity_content["label"]==0:
                      entities_to_delete.append((index, index_entity))

    for i in range(-1, -len(entities_to_delete)-1, -1) :
      index, index_entity = entities_to_delete[i]
      del paragraph_ann['content'][index]['content'][index_entity]

    for index in reversed(paragraphs_to_delete):
      del paragraph_ann['content'][index]

    return paragraph_ann


def fusion(paragraph_ann):
  label = paragraph_ann['label']
  content = ""
  for paragraph in paragraph_ann['content']:
    if type(paragraph['content']) == str :
      content += paragraph['content']
    elif type(paragraph['content']) == list :
      for entity in paragraph['content']:
        content += entity['content']
  json = {
    'label' : label, 
    'content' : content,
  };
  return json
  



p = {
  'label': 1,
  'content': [
    {
      'content':
        "4 crit▒res pour voir o▒ en sont les villes fran▒aises sur les transports et la lutte contre la pollution de l▒air\n",
    },
    {
      'content':
        "Bordeaux, Grenoble, Lille, Lyon, Marseille, Montpellier, Nantes, Nice, Paris, Rennes, Strasbourg, Toulouse : avec l▒appui du R▒seau Action Climat, nous avons ▒valu▒ le positionnement de ces 12 villes sur un abandon progressif des voitures diesel et essence, qui contribuent fortement ▒ la pollution de l▒air et aux changements climatiques. Cela passe par la mise en place de zones ▒ faibles puis tr▒s faibles ▒missions, desquelles sont exclus progressivement les v▒hicules diesel puis essence, d▒ici 2025.\n",
    },
    { 'content': "  D▒COUVREZ O▒ EN EST VOTRE VILLE\n" },
    {
      'content':
        "  Ce panorama r▒unit ▒galement les points de vue et t▒moignages d▒une vingtaine d▒associations locales de promotion du v▒lo et d▒usagers des transports en commun. Nous leur avons demand▒ d▒▒valuer leur ville sur trois enjeux phares de la mobilit▒ durable: renforcement de l▒offre de transports en commun, mise en place d▒un r▒seau express v▒lo, incitations au changement de comportement vers une r▒duction de l▒usage de la voiture individuelle.\n",
    },
    {
      'content':
        "Des villes qui doivent en faire plus pour prot▒ger notre sant▒ et d▒velopper les alternatives ▒ la voiture\n",
    },
    { 'content': "  D▒COUVREZ L'INT▒GRALIT▒ DU PANORAMA AU FORMAT PDF\n" },
    {
      'content':
        "  Ce panorama montre que tr▒s peu de villes se sont engag▒es sur une sortie des v▒hicules diesel et essence. Dans la majorit▒ de ces villes, les associations locales que nous avons sollicit▒es nous disent aussi que l▒action des responsables politiques est insuffisante en mati▒re de d▒veloppement des alternatives ▒ la voiture, telles que le v▒lo ou les transports en commun.\n",
    },
    {
      'content': [
        { 'content': "Pourtant, " },
        {
          'label': 1,
          'content':
            "la pollution de l▒air est aujourd▒hui une v▒ritable urgence de sant▒ publique.",
        },
        {
          'content':
            " Et le trafic routier est en grande partie responsable ! Pour am▒liorer la qualit▒ de l▒air, il faut tr▒s rapidement d▒velopper les alternatives ▒ la voiture individuelle et restreindre la circulation des v▒hicules les plus polluants, diesel et essence.\n",
        },
      ],
    },
    {
      'content':
        "Les grandes villes fran▒aises ont encore du pain sur la planche pour prot▒ger la sant▒ de leurs habitant-e-s et le climat. Les maires de nos grandes villes ont le pouvoir d▒agir pour corriger le tir : demandez-leur de passer ▒ l▒action !\n",
    },
    { 'label': 0, 'content': "SIGNEZ L'APPEL AUX MAIRES\n" },
    {
      'label': 0,
      'content':
        "Retrouvez ci-dessous les pages d▒di▒es aux 12 villes ▒valu▒es :\n",
    },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Bordeaux\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Grenoble\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Lille\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Lyon\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Marseille\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Montpellier\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Nantes\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Nice\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Paris\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Rennes\n" },
    { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Strasbourg\n" },
    {
      'content': [
        { 'label': 0, 'content': "Panorama Mobilit▒ Durable 2018 ▒ Toulouse" },
        { 'label': 1, 'content': "je suis un label 1" },
        { 'label': 0, 'content': "Encore un label 0" },
      ],
    },
  ],
};

# print(remove_useless(p))

# print(fusion(remove_useless(p)))