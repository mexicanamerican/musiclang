


def preprocess(prompt):
    """
    Preprocess the prompt stripping spaces, line return and tabulations
    Parameters
    ----------
    prompt

    Returns
    -------

    """
    return prompt.replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '')

def predict_score_from_hugginface(prompt, temperature=1.0, top_k=20):
    """

    Parameters
    ----------
    prompt

    Returns
    -------

    """
    from transformers import pipeline, GPT2LMHeadModel, GPT2TokenizerFast

    prompt = preprocess(prompt)
    block_size=1024
    hub_model_path = "floriangardin/musiclang"
    predictor = pipeline('text-generation',
                       model=GPT2LMHeadModel.from_pretrained(hub_model_path),
                 tokenizer=GPT2TokenizerFast.from_pretrained(hub_model_path)
                 )

    eos = '<|endoftext|>'
    chord_sep = ')+('
    text = ""
    max_iter = 5
    i = 0

    # We need to keep the first half of the prompt to be able to reconstruct the score
    end_prompt = prompt[-block_size//2:]
    start_prompt = prompt[:-block_size//2]
    prompt = end_prompt
    # Predict until we find ')+(' sequence or we reach the maximum number of iterations

    while not eos in text and (i < max_iter):
        res = predictor(prompt, max_length=block_size, temperature=temperature, do_sample=True, top_k=top_k)[0]['generated_text']
        remaining = block_size//2
        text += res[:remaining]
        prompt = res[remaining:]
        i+= 1

    if i < max_iter:
        return start_prompt + text.split(eos)[0]
    else:
        return start_prompt + chord_sep.join(text.split(chord_sep)[:-1]) + ')'