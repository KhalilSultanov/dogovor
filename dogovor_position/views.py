import os
from django.http import HttpResponse
from django.shortcuts import render
from docx import Document
from docx.shared import Pt
from num2words import num2words


def replace_paragraph_text_with_styles(paragraph, new_text):

    if paragraph.runs:
        style = paragraph.runs[0].style
        font = paragraph.runs[0].font
        is_bold = font.bold
        font_name = font.name
        font_size = font.size
    else:
        is_bold = False
        font_name = 'Calibri'
        font_size = Pt(9)

    paragraph.clear()
    run = paragraph.add_run(new_text)
    run.bold = is_bold
    run.font.name = font_name
    run.font.size = font_size

def handle_additional_work_sections(doc, selected_services, platform_choice):
    # Найти начальный и конечный индексы параграфов для удаления
    start_index, end_index = None, None
    for i, paragraph in enumerate(doc.paragraphs):
        if '{IF_TZ_DELETE}' in paragraph.text:
            start_index = i
        elif '{END_OF_SECTION}' in paragraph.text:
            end_index = i
            break

    if start_index is not None and end_index is not None:
        if 'design_layouts' in selected_services:
            # Удаляем параграфы между start_index и end_index включительно
            for i in range(start_index, end_index + 1)[::-1]:  # В обратном порядке
                p = doc.paragraphs[i]._element
                p.getparent().remove(p)
                p._p = p._element = None
        else:
            for i in [start_index, end_index]:
                paragraph = doc.paragraphs[i]
                text = paragraph.text.replace('{IF_TZ_DELETE}', '').replace('{END_OF_SECTION}', '')
                replace_paragraph_text_with_styles(paragraph, text)

    for paragraph in doc.paragraphs:
        if '{WORD_PRESS}' in paragraph.text or '{NOT_WORD_PRESS}' in paragraph.text:
            if platform_choice == 'wordpress':
                text = paragraph.text.replace('{WORD_PRESS}', 'Работы программиста по результатам коммерческого аудита. Работы программиста после проведения других аудитов включены в счёт').replace('{NOT_WORD_PRESS}', '')
            elif platform_choice == 'not_wordpress':
                text = paragraph.text.replace('{WORD_PRESS}', '').replace('{NOT_WORD_PRESS}', 'Работы программиста.')
            else:
                text = paragraph.text.replace('{WORD_PRESS}', '').replace('{NOT_WORD_PRESS}', '')
            replace_paragraph_text_with_styles(paragraph, text)


def calculate_and_replace_tags_10(doc, request):
    req_count_top10 = int(request.POST.get('req_count_top10'))
    region_name = request.POST.get('region_name')
    search_engine = request.POST.get('search_engine')

    # Определяем базовую стоимость запроса в зависимости от региона
    if region_name in ['СПб', 'Мск']:
        req_pay = 300  # Цена за запрос в топ-10 для СПб и Мск
    else:
        req_pay = 200  # Цена за запрос в топ-10 для других регионов

    # Увеличиваем стоимость на 100 руб., если поисковик Google
    if search_engine == 'GOOGLE':
        req_pay += 100

    # Замена меток стоимости запроса
    replace_tag_with_text(doc, '{REQ_PAY_10}', str(req_pay))
    replace_tag_with_text(doc, '{REQ_PAY_WORDS_10}', num2words(req_pay, lang='ru'))

    # Расчет и замена меток для премий
    total_premium = req_pay * req_count_top10
    for i in range(10, 101, 10):
        percent = i / 100
        tag = '{PREM_TOP10_' + str(i) + '}'
        prem_value = int(total_premium * percent)
        replace_tag_with_text(doc, tag, str(prem_value))

def calculate_and_replace_tags_5(doc, request):
    req_count_top5 = int(request.POST.get('req_count_top5'))
    region_name = request.POST.get('region_name')
    search_engine = request.POST.get('search_engine')

    # Определяем базовую стоимость запроса в зависимости от региона
    if region_name in ['СПб', 'Мск']:
        req_pay = 500  # Цена за запрос в топ-10 для СПб и Мск
    else:
        req_pay = 250  # Цена за запрос в топ-10 для других регионов

    # Увеличиваем стоимость на 100 руб., если поисковик Google
    if search_engine == 'GOOGLE':
        req_pay += 100

    # Замена меток стоимости запроса
    replace_tag_with_text(doc, '{REQ_PAY_5}', str(req_pay))
    replace_tag_with_text(doc, '{REQ_PAY_WORDS_5}', num2words(req_pay, lang='ru'))

    # Расчет и замена меток для премий
    total_premium = req_pay * req_count_top5
    for i in range(10, 101, 10):
        percent = i / 100
        tag = '{PREM_TOP5_' + str(i) + '}'
        prem_value = int(total_premium * percent)
        replace_tag_with_text(doc, tag, str(prem_value))

def calculate_and_replace_tags_3(doc, request):
    req_count_top3 = int(request.POST.get('req_count_top3'))
    region_name = request.POST.get('region_name')
    search_engine = request.POST.get('search_engine')

    # Определяем базовую стоимость запроса в зависимости от региона
    if region_name in ['СПб', 'Мск']:
        req_pay = 600  # Цена за запрос в топ-10 для СПб и Мск
    else:
        req_pay = 300  # Цена за запрос в топ-10 для других регионов

    # Увеличиваем стоимость на 100 руб., если поисковик Google
    if search_engine == 'GOOGLE':
        req_pay += 100

    # Замена меток стоимости запроса
    replace_tag_with_text(doc, '{REQ_PAY_3}', str(req_pay))
    replace_tag_with_text(doc, '{REQ_PAY_WORDS_3}', num2words(req_pay, lang='ru'))

    # Расчет и замена меток для премий
    total_premium = req_pay * req_count_top3
    for i in range(10, 101, 10):
        percent = i / 100
        tag = '{PREM_TOP3_' + str(i) + '}'
        prem_value = int(total_premium * percent)
        replace_tag_with_text(doc, tag, str(prem_value))


def handle_conditional_sections(doc, edo):
    edo_text_1 = "(в том числе его получения с использованием системы электронного документооборота)" if edo == "YES" else ""
    edo_text_2 = (
                "10.4. Стороны согласовали, что они вправе осуществлять документооборот в электронном виде по телекоммуникационным каналам связи с использованием усиленной квалификационной электронной подписи посредством системы электронного документооборота СБИС. " + "\n" +
                "10.4.1. В целях настоящего договора под электронным документом понимается документ, созданный в электронной форме без предварительного документирования на бумажном носителе, подписанный электронной подписью в порядке, установленном законодательством Российской Федерации. Стороны признают электронные документы, заверенные электронной подпись, при соблюдении требований Федерального закона от 06.04.2011 № 63-ФЗ 'Об электронной подписи' юридически эквивалентным документам на бумажных носителях, заверенным соответствующими подписями и оттиском печатей Сторон. " + "\n" +
                "10.5. Все изменения и дополнения к договору оформляются в виде дополнений и приложений к договору, являющийся его неотъемлемой частью." + "\n" +
                " 10.6. Договор составлен в двух подлинных экземплярах, имеющих одинаковую юридическую силу, по одному для каждой из сторон. ") \
        if edo == "YES" else ""
    not_edo_text = "на почту Исполнителя" if edo == "NO" else ""

    write_by_hand = (
                "10.4. Все изменения и дополнения к договору оформляются в виде дополнений и приложений к договору, являющийся его неотъемлемой частью. " + '\n' +
                "10.5. Договор составлен в двух подлинных экземплярах, имеющих одинаковую юридическую силу, по одному для каждой из сторон.)") if edo == "NO" else ""

    replacements = {
        '{EDO_1}': edo_text_1,
        '{EDO_2}': edo_text_2,
        '{NOT_EDO}': not_edo_text,
        '{WRITE_BY_HAND}': write_by_hand
    }


    for paragraph in doc.paragraphs:
        for tag, replacement in replacements.items():
            if tag in paragraph.text:
                paragraph_text = paragraph.text.replace(tag, replacement)
                replace_paragraph_text_with_styles(paragraph, paragraph_text)




def replace_tag_with_text(doc, tag, text=None):
    for paragraph in doc.paragraphs:
        if tag in paragraph.text:
            new_text = paragraph.text.replace(tag, text if text is not None else '').strip()
            if new_text:
                replace_paragraph_text_with_styles(paragraph, new_text)
            else:
                # Если параграф остался пустым, удаляем его
                p = paragraph._element
                p.getparent().remove(p)
                p._p = p._element = None

def process_contract(request):
    if request.method == 'POST':

        service_to_tag_mapping = {
            'optimization_headers': ('{HEAD_PAGES}', '- Оптимизация заголовков страниц;'),
            'optimization_metatags': ('{METATAGS}', '- Оптимизация метатегов;'),
            'writing_optimization': ('{NEURO}', '- Написание текстов с помощью нейросетей и их оптимизация;'),
            'site_structure_optimization': ('{STRUCTURE}', '- Оптимизация структуры сайта;'),
            'technical_error_fixing': ('{FIX}', '- Устранение технических ошибок на сайте;'),
            'design_layouts': ('{TZ}', '- Техническое задание (ТЗ) на создание дизайн-макетов отдельных блоков или страниц на сайте;'),
            'creating_pages': ('{CREATE_PAGES}', '- Создание страниц на сайте;')
        }

        contract_number = request.POST.get('contract_number')
        date_day = request.POST.get('date_day')
        site_name = request.POST.get('site_name')
        region_name = request.POST.get('region_name', 'СПб')
        custom_region_name = request.POST.get('custom_region_name', '').strip()

        if region_name == 'Другой' and custom_region_name:
            region_name = custom_region_name
        search_engine = request.POST.get('search_engine', 'YANDEX')


        price_count_digit = request.POST.get('price_count_digit')
        price_count_word = num2words(price_count_digit, lang='ru')

        date_month = request.POST.get('date_month')
        date_year = request.POST.get('date_year')
        organization_name = request.POST.get('organization_name')
        reason = request.POST.get('reason')
        person_name = request.POST.get('person_name')
        director_name = request.POST.get('director_name')
        email = request.POST.get('email')
        inn = request.POST.get('inn')
        ogrn = request.POST.get('ogrn')
        registration_address = request.POST.get('registration_address')
        checking_account = request.POST.get('checking_account')
        correspondent_account = request.POST.get('correspondent_account')
        bank_name = request.POST.get('bank_name')
        bic = request.POST.get('bic')
        edo = request.POST.get('edo')
        req_count_top10 = request.POST.get('req_count_top10')
        req_count_top5 = request.POST.get('req_count_top5')
        req_count_top3 = request.POST.get('req_count_top3')
        topvisor = request.POST.get('topvisor')

        support_options = request.POST.getlist('support[]')
        platform_choice = request.POST.get('platform', None)
        selected_services = request.POST.getlist('services[]')



        template_filename = 'Договор Позиции метки.docx'
        template_path = os.path.join(os.path.dirname(__file__), '../dogovora', template_filename)
        doc = Document(template_path)

        calculate_and_replace_tags_10(doc, request)
        calculate_and_replace_tags_5(doc, request)
        calculate_and_replace_tags_3(doc, request)

        for paragraph in doc.paragraphs:
            if '{YANDEX}' in paragraph.text or '{GOOGLE}' in paragraph.text:
                if search_engine == 'YANDEX':
                    paragraph_text = paragraph.text.replace('{YANDEX}', 'Яндекс').replace('{GOOGLE}', '')
                else:
                    paragraph_text = paragraph.text.replace('{YANDEX}', '').replace('{GOOGLE}', 'Google')
                replace_paragraph_text_with_styles(paragraph, paragraph_text)

        for paragraph in doc.paragraphs:
            if search_engine == 'YANDEX':
                if 'Google Search' in paragraph.text or 'Google Analytics' in paragraph.text:
                    new_text = paragraph.text.replace(' и Google Search', '').replace(' и Google Analytics', '')
                    new_text = new_text.replace(' и ,', '').replace('  ', ' ')
                    replace_paragraph_text_with_styles(paragraph, new_text.strip())
        for paragraph in doc.paragraphs:
            if '{REGION_NAME}' in paragraph.text:
                paragraph_text = paragraph.text.replace('{REGION_NAME}', region_name)
                replace_paragraph_text_with_styles(paragraph, paragraph_text)


        if 'support_site' in support_options:
            support_text = '- Поддержка сайта в техническом плане;'
            replace_tag_with_text(doc, '{SITE_SUPPORT}', support_text)
        else:
            replace_tag_with_text(doc, '{SITE_SUPPORT}')

        used_tags = set()

        for service_key in selected_services:
            if service_key in service_to_tag_mapping:
                tag, text = service_to_tag_mapping[service_key]
                replace_tag_with_text(doc, tag, text)
                used_tags.add(tag)

        all_tags = set(service_to_tag_mapping.values())
        unused_tags = {tag for tag, _ in all_tags if tag not in used_tags}
        for tag in unused_tags:
            replace_tag_with_text(doc, tag)


        handle_conditional_sections(doc, edo)
        handle_additional_work_sections(doc, selected_services, platform_choice)

        footer = doc.sections[0].footer
        for paragraph in footer.paragraphs:
            paragraph.alignment = 1
            for run in paragraph.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(9)
        paragraph = footer.paragraphs[0]
        paragraph.add_run("________________" + director_name + "").font.size = Pt(12)
        paragraph.add_run("                                                                           ").font.size = Pt(
            12)
        paragraph.add_run("_______________Михайлов Д.С.").font.size = Pt(12)

        replacements = {
            '{DOGOVOR_NUMBER}': contract_number,
            '{DAY}': date_day,
            '{MONTH}': date_month,
            '{YEAR}': date_year,
            '{CUSTOMER_ORGANIZATION}': organization_name,
            '{CUSTOMER_FIO}': person_name,
            '{DOGOVOR_OSNOVANIE}': reason,

            '{SITE_NAME}': site_name,
            '{REGION_NAME}': region_name,
            '{PRICE_COUNT}': price_count_digit,
            '{PRICE_COUNT_IN_WORDS}': price_count_word,


            '{FIO_DIRECTOR}': director_name,
            '{CUSTOMER_EMAIL}': email,
            '{CUSTOMER_NAME}': organization_name,
            '{INN}': inn,
            '{OGRN}': ogrn,
            '{REGISTRATION_ADDRESS}': registration_address,
            '{PAYMENT_ACCOUNT}': checking_account,
            '{CORRESPONDENT}': correspondent_account,
            '{BANK_NAME}': bank_name,
            '{BIK}': bic,
            '{REQ_COUNT_TOP10}': req_count_top10,
            '{REQ_COUNT_TOP5}': req_count_top5,
            '{REQ_COUNT_TOP3}': req_count_top3,
            '{TOPVISOR}': topvisor,
        }

        for paragraph in doc.paragraphs:
            for key, value in replacements.items():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(key, str(value))
                    for run in paragraph.runs:
                        run.font.name = 'Calibri'
                        run.font.size = Pt(9)
                        if key == '{DOGOVOR_NUMBER}' or key == '{CUSTOMER_NAME}':
                            run.bold = True

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for key, value in replacements.items():
                            if key in paragraph.text:
                                paragraph.text = paragraph.text.replace(key, value)
                                for run in paragraph.runs:
                                    run.font.name = 'Calibri'
                                    run.font.size = Pt(9)
                                    if run.text.strip() == value:
                                        run.bold = True

        for section in doc.sections:
            footer = section.footer
            for paragraph in footer.paragraphs:
                paragraph.alignment = 1
                for run in paragraph.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(9)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="processed_contract.docx"'
        doc.save(response)
        return response
    else:
        return render(request, 'dogovor_position_form.html')
