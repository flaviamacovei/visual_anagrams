import inflect

p = inflect.engine()

def create_system_prompt_is_1(views, goals):
    prompt = (f"This image has been generated to depict an optical illusion. It has {p.number_to_words(len(goals))} "
            f"views and {p.number_to_words(len(goals))} corresponding goals. You can see all "
            f"{p.number_to_words(len(goals))} images in their corresponding view. It is your job to determine if "
            f"the images show \"independent synthesis\". This means that all goals are distinguishable in all views. "
            f"If you can make out goal 1 in view 2, and goal 2 in view 1 and so on, this is an indication of "
            f"independent synthesis. Please analyse these images and detect whether this effect occurs. Output "
            f"your answer in the following format:\n"
            f"<yes/no>---<any text or explanation>\n"
            f"So for example if the image shows independent synthesis, a valid output would be \"yes---I can "
            f"detect both a rabbit and a goose in both views.\"\n"
            f"Here are the views and goals:\n")
    for i, (view, goal) in enumerate(zip(views, goals)):
        prompt += f"View {i + 1}: {view[1]}; Goal {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_is_2(views, goals):
    prompt = f"This image consists of {p.number_to_words(len(goals))} sub-images.\n"
    for i, goal in reversed(list(enumerate(goals))):
        for j in range(len(goals)):
            if i != j:
                prompt += f"Can you detect {goal} in the {p.ordinal(j + 1)} subimage?\n"
    prompt += ("If you can answer all of these questions with yes, please just say \"yes---<any text or explanation>\" "
                f"otherwise say \"no---<any text or explanation>\"\n"
                f"So for example if the image , a valid output would be \"yes---I can "
                f"detect both a rabbit and a goose in both sub-images.\"")
    return prompt

def create_system_prompt_is_3(views, goals):
    prompt = (f"The following image consists of {p.number_to_words(len(goals))} subimages. Please separate the "
            f"subimages when analysing. The images are one and the same but with some transformation applied "
            f"to the pixels so that what you see in the subimages changes. Your objective is to find out if this "
            f"is achieved correctly. Specifically, I want you to check for \"independent synthesis\". Independent "
            f"symthesis means that all goal images are discernable in all views. I will give you a list of target "
            f"images and you have to check for independent synthesis. Match the first view and target to the "
            f"first subimage, the second target image to the second subimage, etc. and tell me if you can detect "
            f"any independent synthesis.\nIt is very important that you output your answer in the following format:\n"
            f"<yes/no>---<any text or exlanation>\n"
            f"So for example if the image shows independent synthesis, a valid output would be \"yes---I can "
            f"detect both a rabbit and a goose in both sub-images.\"\n"
            f"Here are the target images:\n")
    for i, (view, goal) in enumerate(zip(views, goals)):
        prompt += f"Target {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_is_4(views, goals):
    prompt = (f"The image you are given has been generated using an AI model to depict an optical illusion: "
            f"When viewed under specific transformations, it appears to show different things. We will call those "
            f"targets. Your objective is to analyise this image and detect whether it shows any \"independent "
            f"synthesis\". This means that all targets are visible in all views, not just its own. All "
            f"transformations are already applied and concatenated, resulting in an image with "
            f"{p.number_to_words(len(goals))} subimages. You will be given a list of targets and have to analyse "
            f"if the targets are discernable in all other views.\n"
            f"Please output your response in the form <yes/no>---<any text or explanation>\n"
            f"So for example if the image shows independent synthesis, a valid output would be \"yes---I can "
            f"detect both a rabbit and a goose in both sub-images.\"\n"
            f"Here are the target images:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_is_5(views, goals):
    prompt = (f"You are analyzing an image that has been split into {p.number_to_words(len(goals))} subimages. "
              f"Each subimage corresponds to a target. Your task is to evaluate if all target images are detectable "
              f"in all subimages. This phenomenon is referred to as \"independent synthesis.\" For each subimage, "
              f"check if it contains a target image that belongs to a different subimage.\n"
              f"Provide your output as follows: <yes/no>---<any text or explanation>\n"
              f"For example: \"yes---I can detect both a rabbit and a goose in both subimages.\"\n"
              f"Here are the target images:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt


prompt_functions_is = [create_system_prompt_is_1, create_system_prompt_is_2, create_system_prompt_is_3, create_system_prompt_is_4, create_system_prompt_is_5]
#prompt_functions_is = [create_system_prompt_is_1]

def create_system_prompt_ss_1(views, goals):
    prompt = (f"This image conssits of {p.number_to_words(len(goals))} subimages. You will be given a list of targets that "
            f"correspond to each subimage. Your objective is to detect if the image shows signs of \"solitary synthesis\" "
            f"which means that one target is achieved to a significantly higher degree than the others. One indication is "
            f"that you can discern a target in a subimage other than its corresponding one. It would also be that for one "
            f"sub-image, you can't depict its target in it. Please analyze the image and tell me if you detect solitary "
            f"synthesis. It is important that you output your response in the following format:\n"
            f"<yes/no>---<any text or explanation>\n"
            f"For example: \"yes---the first target of a horse is much more pronounced than the other target.\"\n"
            f"Here are the target images:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_ss_2(views, goals):
    prompt = (f"The image you are given has been generated using an AI model to depict an optical illusion. When viewes under "
            f"different transformations, a different target becomes apparent. The transformations have been applied and "
            f"concatenated to create an array of {p.number_to_words(len(goals))} subimages. It is your job to detect an error "
            f"called \"solitary synthesis\" where one target is more pronounced than the other{'s' if len(goals) > 2 else ''}. "
            f"Please analyze these images and tell me if you can detect one specific target from views other than its own.\n"
            f"Please output your conclusion in the following format:\n"
            f"<yes/no>---<any text or explanation>\n"
            f"For example: \"yes---the first target of a horse is much more pronounced than the other target.\"\n"
            f"Here are the target images:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_ss_3(views, goals):
    prompt = (f"The given image is divided into {p.number_to_words(len(goals))} subimages, each representing a unique target. "
              f"Your goal is to detect an anomaly known as \"solitary synthesis.\" This occurs when one target becomes "
              f"significantly more prominent than others, either by appearing in additional subimages or by overshadowing "
              f"its counterparts entirely. You should also consider if a target is missing from its intended subimage.\n"
              f"Carefully analyze all subimages and provide your conclusion in this exact format:\n"
              f"<yes/no>---<any text or explanation>\n"
              f"For instance: \"yes---the first target, a horse, is far more distinct compared to the other targets.\"\n"
              f"The targets for each subimage are listed below:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_ss_4(views, goals):
    prompt = (f"You are tasked with evaluating an image composed of {p.number_to_words(len(goals))} subimages. Each subimage "
              f"was generated to depict a specific target. Your objective is to identify a phenomenon called \"solitary synthesis,\" "
              f"where one target dominates in clarity or appears in unrelated subimages, disrupting the intended balance.\n"
              f"Analyze the subimages to determine if this effect is present. Pay attention to whether any target is missing or "
              f"overly dominant. Ensure your response follows this strict format:\n"
              f"<yes/no>---<any text or explanation>\n"
              f"For example: \"yes---the first target, a horse, overshadows the other targets across multiple subimages.\"\n"
              f"Here are the targets for the subimages:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_ss_5(views, goals):
    prompt = (f"This image consists of {p.number_to_words(len(goals))} subimages, each designed to display a unique target "
              f"under specific transformations. However, there is a risk of \"solitary synthesis,\" where one target "
              f"becomes disproportionately dominant, either by being detectable in unrelated subimages or by completely "
              f"masking others.\n"
              f"Your task is to analyze the subimages and identify if solitary synthesis occurs. If it does, provide your "
              f"reasoning. Use the following response format:\n"
              f"<yes/no>---<any text or explanation>\n"
              f"Example: \"yes---the target of a horse in the first subimage is overwhelmingly more distinct than the rest.\"\n"
              f"The targets for each subimage are as follows:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"
    return prompt

def create_system_prompt_ss_6(views, goals):
    prompt = (f"The image you are given has been generated using an AI model to depict an optical illusion: "
            f"When viewed under specific transformations, it appears to show different things. We will call those "
            f"targets. Your objective is to analyise this image and detect whether it shows any \"solitary "
            f"synthesis\". This means that one target is visible in views other than its own. All "
            f"transformations are already applied and concatenated, resulting in an image with "
            f"{p.number_to_words(len(goals))} subimages. You will be given a list of targets and have to analyse "
            f"if the targets are discernable in all other views.\n"
            f"Please output your response in the form <yes/no>---<any text or explanation>\n"
            f"So for example if the image shows independent synthesis, a valid output would be \"yes---I can "
            f"detect both a rabbit and a goose in both sub-images.\"\n"
            f"Here are the target images:\n")
    for i, goal in enumerate(goals):
        prompt += f"Subimage {i + 1}: {goal}\n"

prompt_functions_ss = [create_system_prompt_ss_1, create_system_prompt_ss_2, create_system_prompt_ss_3, create_system_prompt_ss_4, create_system_prompt_ss_5, create_system_prompt_ss_6]
# prompt_functions_ss = [create_system_prompt_ss_1]
