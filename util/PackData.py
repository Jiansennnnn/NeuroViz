import json 

def PackDataToJson(structured_report, img_path,chart_base64, idea):
    ##Idea context cleanup
    raw_ideas_json_str = idea
    cleaned_ideas_json_str = raw_ideas_json_str.replace('```json\n', '').replace('\n```', '')
    try:
        structured_ideas = json.loads(cleaned_ideas_json_str)
        #print(structured_ideas)  # Output the result to verify
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

    
    packed_data = {
        "report": structured_report,
        "Img_path": {
            "histogram": img_path['histogram_img_path'],
            "scatter": img_path['scatter_img_path']
            },
        "Chart Base64": chart_base64,
        "Ideas": structured_ideas
    }
    

    
    
    # dump content to json
    json_report = json.dumps(packed_data, indent=4, ensure_ascii=False)

    return json_report