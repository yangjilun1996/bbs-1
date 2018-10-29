@reset.route('/test', methods=['GET', 'POST'])
def home():
    li = get_reset_record()

    pager_obj = Pagination(request.args.get('page', 1), len(li), request.path, request.args, per_page_count=20)
    index_list = li[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render_template('common/result_install.html', index_list=index_list, html=html)
