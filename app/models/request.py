from app.utils.helper2 import valid_language
from app.managers.find_language import Finder
from app.managers.api_call import Translator
from app.utils.lang_code import lang_code


class Request:
    def __init__(self):
        pass

    def request_handeler(self, request_data, api_name):
        ans = {'error': 0}
        source_language = request_data.get("source_language").lower().strip()
        print("google_apit called")

        finder = Finder()
        translated_txt = finder.api_call(request_data)
        if translated_txt['error']:
            return translated_txt
        detected_language = translated_txt['detected_language']

        # Checking if source language is given
        if len(source_language.strip()) > 0:
            # Checking for valid language
            if not valid_language(source_language):
                ans['error'] = 1
                ans["error_message"] = "API does not support {} language as source language".format(source_language)
                return ans
            elif detected_language.lower() != source_language.lower():
                ans['error'] = 1
                ans['error_message'] = 'Detected Language doesnot match with Source Language'
                return ans
        ans['source_language'] = detected_language
        request_data['source_language'] = detected_language
        target_language = request_data.get('target_language').lower().strip()
        ans['target_language'] = target_language
        # checking if target language is valid or not
        if not valid_language(target_language):
            ans['error'] = 1
            ans["error_message"] = "API does not support {} language as target language".format(target_language)

        if ans['error'] == 1:
            return ans

        translator = Translator()
        response_ = translator.api_call(request_data, api_name)
        return response_


    def suggestion_handler(self,request_data):
        suggestions = []
        print("Suggestion is called")
        target_string = request_data.get('text')
        n = len(target_string)
        if not n:
            return suggestions
        for word in lang_code.keys():
            if target_string.lower() == word[:n].lower():
                suggestions.append(word)
        if len(suggestions) > 10:
            suggestions = suggestions[:10]
        sugg = {'suggestion': suggestions}
        return sugg
