import flet as ft
from datetime import datetime
from database import Database

def main(page: ft.Page):
    db = Database()
    page.title = "GERENCIADOR DE COTAÇÕES | Criado por ROBSON BEZERRA | robsonb0819@gmail.com"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 950
    page.padding = 5
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_color=ft.Colors.BLUE_ACCENT,
            thickness=8,
            main_axis_margin=5,
            thumb_visibility=True
        )
    )


    # FUNÇÃO PARA FAZER BACKUP, USANDO O MÉTODO DA CLASSE DATABASE
    def fazer_backup(e):
        sucesso, mensagem = db.backup()
        print(f"BACKUP - Sucesso: {sucesso}, Mensagem: {mensagem}")  # debug no terminal
        page.snack_bar = ft.SnackBar(
            ft.Text(mensagem),
            bgcolor=ft.Colors.GREEN if sucesso else ft.Colors.RED,
            duration=5000
        )
        page.snack_bar.open = True
        page.update()


    list_view = ft.ListView(expand=True, spacing=10)



    # VARIÁVEIS PARA FILTROS E ORDENAÇÃO
    termo_busca_projeto = ""
    termo_busca_so = ""
    termo_busca_cliente = ""
    ordenacao_cliente = 0
    ordenacao_prazo = 0
    ordenacao_urgencia = 0


    # FILTROS

    def buscarPor_projeto(e):
        nonlocal termo_busca_projeto
        termo_busca_projeto = e.control.value.strip().lower()
        renderizar_tudo()

    def buscarPor_so(e):
        nonlocal termo_busca_so
        termo_busca_so = e.control.value.strip().lower()
        renderizar_tudo()

    def buscarPor_cliente(e):
        nonlocal termo_busca_cliente
        termo_busca_cliente = e.control.value.strip().lower()
        renderizar_tudo()

    def limpar_filtros(e):
        nonlocal termo_busca_projeto, termo_busca_so, termo_busca_cliente
        termo_busca_cliente = ""
        termo_busca_projeto = ""
        termo_busca_so = ""
        input_busca_projeto.value = ""
        input_busca_so.value = ""
        input_busca_cliente.value = ""
        renderizar_tudo()

    def alternar_ordenacao_cliente(e):
        nonlocal ordenacao_cliente, ordenacao_prazo, ordenacao_urgencia
        ordenacao_cliente = (ordenacao_cliente + 1) % 3
        ordenacao_prazo = 0
        ordenacao_urgencia = 0
        if ordenacao_cliente == 0:
            btn_ordenar_cliente.icon = ft.Icons.SORT
            btn_ordenar_cliente.tooltip = "Ordenar por cliente (A-Z)"
            btn_ordenar_cliente.icon_color = ft.Colors.BLUE_ACCENT
        elif ordenacao_cliente == 1:
            btn_ordenar_cliente.icon = ft.Icons.SORT_BY_ALPHA
            btn_ordenar_cliente.tooltip = "Orden crescente (A-Z) - clique para decrescente"
            btn_ordenar_cliente.icon_color = ft.Colors.BLUE_ACCENT
        else:
            btn_ordenar_cliente.icon = ft.Icons.SORT_BY_ALPHA
            btn_ordenar_cliente.icon_color = ft.Colors.RED_400
            btn_ordenar_cliente.tooltip = "Orden decrescente (Z-A) - clique para padrão"
        btn_ordenar_prazo.icon = ft.Icons.SORT
        btn_ordenar_prazo.icon_color = ft.Colors.BLUE_ACCENT
        btn_ordenar_prazo.tooltip = "Ordenar por prazo final"
        btn_ordenar_urgencia.icon = ft.Icons.SORT
        btn_ordenar_urgencia.icon_color = ft.Colors.BLUE_ACCENT
        btn_ordenar_urgencia.tooltip = "Ordenar por urgência (Alta primeiro)"
        renderizar_tudo()

    def alternar_ordenacao_prazo(e):
        nonlocal ordenacao_prazo, ordenacao_cliente, ordenacao_urgencia
        ordenacao_prazo = (ordenacao_prazo + 1) % 3
        ordenacao_cliente = 0
        ordenacao_urgencia = 0
        if ordenacao_prazo == 0:
            btn_ordenar_prazo.icon = ft.Icons.SORT
            btn_ordenar_prazo.tooltip = "Ordenar por prazo final"
            btn_ordenar_prazo.icon_color = ft.Colors.BLUE_ACCENT
        elif ordenacao_prazo == 1:
            btn_ordenar_prazo.icon = ft.Icons.SORT_BY_ALPHA
            btn_ordenar_prazo.tooltip = "Prazo mais próximo primeiro"
            btn_ordenar_prazo.icon_color = ft.Colors.BLUE_ACCENT
        else:
            btn_ordenar_prazo.icon = ft.Icons.SORT_BY_ALPHA
            btn_ordenar_prazo.icon_color = ft.Colors.RED_400
            btn_ordenar_prazo.tooltip = "Prazo mais distante primeiro"
        btn_ordenar_cliente.icon = ft.Icons.SORT
        btn_ordenar_cliente.icon_color = ft.Colors.BLUE_ACCENT
        btn_ordenar_cliente.tooltip = "Ordenar por cliente (A-Z)"
        btn_ordenar_urgencia.icon = ft.Icons.SORT
        btn_ordenar_urgencia.icon_color = ft.Colors.BLUE_ACCENT
        btn_ordenar_urgencia.tooltip = "Ordenar por urgência (Alta primeiro)"
        renderizar_tudo()

    def alternar_ordenacao_urgencia(e):
        nonlocal ordenacao_urgencia, ordenacao_cliente, ordenacao_prazo
        ordenacao_urgencia = (ordenacao_urgencia + 1) % 3
        ordenacao_cliente = 0
        ordenacao_prazo = 0
        if ordenacao_urgencia == 0:
            btn_ordenar_urgencia.icon = ft.Icons.SORT
            btn_ordenar_urgencia.tooltip = "Ordenar por urgência (Alta primeiro)"
            btn_ordenar_urgencia.icon_color = ft.Colors.BLUE_ACCENT
        elif ordenacao_urgencia == 1:
            btn_ordenar_urgencia.icon = ft.Icons.SORT_BY_ALPHA
            btn_ordenar_urgencia.tooltip = "Urgência ALTA primeiro"
            btn_ordenar_urgencia.icon_color = ft.Colors.BLUE_ACCENT
        else:
            btn_ordenar_urgencia.icon = ft.Icons.SORT_BY_ALPHA
            btn_ordenar_urgencia.icon_color = ft.Colors.RED_400
            btn_ordenar_urgencia.tooltip = "Urgência BAIXA primeiro"
        btn_ordenar_cliente.icon = ft.Icons.SORT
        btn_ordenar_cliente.icon_color = ft.Colors.BLUE_ACCENT
        btn_ordenar_cliente.tooltip = "Ordenar por cliente (A-Z)"
        btn_ordenar_prazo.icon = ft.Icons.SORT
        btn_ordenar_prazo.icon_color = ft.Colors.BLUE_ACCENT
        btn_ordenar_prazo.tooltip = "Ordenar por prazo final"
        renderizar_tudo()


    # DATE PICKER
    
    def on_date_change(e):
        if e.control.value:
            input_prazo.value = e.control.value.strftime("%d/%m/%Y")
            page.update()

    pegarData = ft.DatePicker(on_change=on_date_change)
    page.overlay.append(pegarData)


    #FUNÇÃO PARA O BOTÃO ABRIR CALENDÁRIO

    def abrir_calendario(e): 
        pegarData.open = True
        page.update()



    #FUNÇÃO PARA ORDENAÇÃO DAS DATAS NO ELIF DE ORDENAÇÃO POR PRAZO (DATAS)
    
    def converter_data(data_str):
        if not data_str:
            return None
        try:
            return datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            return None
    
    

    def renderizar_tudo():
        list_view.controls.clear()
        todas = db.listar_cotacoes()

        cotacoes_filtradas = todas[:]
        if termo_busca_projeto:
            cotacoes_filtradas = [row for row in cotacoes_filtradas if row[3] and termo_busca_projeto in row[3].lower()]
        if termo_busca_so:
            cotacoes_filtradas = [row for row in cotacoes_filtradas if row[4] and termo_busca_so in row[4].lower()]
        if termo_busca_cliente:
            cotacoes_filtradas = [row for row in cotacoes_filtradas if row[2] and termo_busca_cliente in row[2].lower()]

        if ordenacao_urgencia == 1:
            cotacoes_filtradas.sort(key=lambda row: row[5], reverse=True)
        elif ordenacao_urgencia == 2:
            cotacoes_filtradas.sort(key=lambda row: row[5])
        
        elif ordenacao_cliente == 1:
            cotacoes_filtradas.sort(key=lambda row: (row[2] or "").lower())
        elif ordenacao_cliente == 2:
            cotacoes_filtradas.sort(key=lambda row: (row[2] or "").lower(), reverse=True)
        
        elif ordenacao_prazo == 1:
            cotacoes_filtradas.sort(key=lambda row: (
                converter_data(row[8]) is None,
                converter_data(row[8]) if converter_data(row[8]) else datetime.max
            ))
        elif ordenacao_prazo == 2:
            cotacoes_filtradas.sort(key=lambda row: (
                converter_data(row[8]) is None,
                -converter_data(row[8]).toordinal() if converter_data(row[8]) else 0
            ))


        for row in cotacoes_filtradas:
            (cotacao_id, data_registro, cliente, projeto, so, urgencia, modal,
             descricao, prazo_final, contato, origem, destino, dimensoes, peso,
             observacao, followup) = row

            cliente_texto = cliente if cliente else "Cliente não informado"
            so_texto = so if so else "N/A"
            urg_color = ft.Colors.BLUE if urgencia == 0 else ft.Colors.RED
            urg_texto = "Baixa" if urgencia == 0 else "Alta"

            modal_texto = modal if modal else "Não especificado"
            modal_icon = {
                "rodoviário": ft.Icons.LOCAL_SHIPPING,
                "ferroviário": ft.Icons.TRAIN,
                "marítimo": ft.Icons.DIRECTIONS_BOAT,
                "fluvial": ft.Icons.WATER,
                "aéreo": ft.Icons.FLIGHT,
                "multimodal": ft.Icons.ROUTER
            }.get(modal, ft.Icons.QUESTION_MARK)

            prazo_texto = prazo_final if prazo_final else "Sem prazo"
            contato_texto = contato if contato else "N/A"
            origem_texto = origem if origem else "N/A"
            destino_texto = destino if destino else "N/A"
            dimensoes_texto = dimensoes if dimensoes else "N/A"
            peso_texto = peso if peso else "N/A"
            observacao_texto = observacao if observacao else ""
            followup_texto = followup if followup else "Sem follow-up"

            card_content = ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PERSON, size=16, color=ft.Colors.GREY_700),
                    ft.Text(f"CLIENTE: {cliente_texto}", size=16, weight="bold", expand=True),
                    ft.Icon(ft.Icons.BUSINESS, size=16, color=ft.Colors.BLUE_GREY_700),
                    ft.Text(f"PROJETO: {projeto}", size=16, weight="bold", expand=True),
                    ft.Icon(ft.Icons.CALENDAR_TODAY, size=14, color=ft.Colors.GREY_600),
                    ft.Text(f"REGISTRADO EM: {data_registro}", size=13, color=ft.Colors.GREY_600),
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, tid=cotacao_id: abrirModalEdicao(tid)),
                    ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, tid=cotacao_id: deletar(tid)),
                ]),
                ft.Row([
                    ft.Icon(ft.Icons.EVENT_AVAILABLE, size=16, color=urg_color),
                    ft.Text(f"PRAZO FINAL: {prazo_texto}", size=14),
                    ft.VerticalDivider(width=10, thickness=5),
                    ft.Text(f"URGÊNCIA: {urg_texto}", size=12, color=urg_color),
                    ft.VerticalDivider(width=10, thickness=5),
                    ft.Text(f"DESCRIÇÃO: {descricao}", size=14, color=ft.Colors.BLACK),
                    ft.VerticalDivider(width=10, thickness=5),
                    ft.Icon(ft.Icons.ASSIGNMENT_LATE, size=14, color=ft.Colors.GREY_700),
                    ft.Text(f"S.O.: {so_texto}", size=13, italic=True),
                    ft.VerticalDivider(width=10, thickness=5),
                    ft.Icon(modal_icon, size=16, color=ft.Colors.GREEN),
                    ft.Text(f"MODAL: {modal_texto.capitalize()}", size=13),
                ]),
                ft.Row([
                    ft.Icon(ft.Icons.NOTES, size=14, color=ft.Colors.BLUE_GREY_700),
                    ft.Text(f"OBSERVAÇÃO: {observacao_texto}", size=13, width=1030)
                ]),
                ft.Container(
                    height=80,
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[ft.Text(f"FOLLOW-UP:\n{followup_texto}", size=14, color=ft.Colors.GREY_800)]
                    ),
                    border=ft.Border.all(0.3, ft.Colors.BLUE_GREY_700),
                    padding=5,
                ),
                ft.Row([
                    ft.Icon(ft.Icons.PERSON, size=14, color=ft.Colors.GREY_700),
                    ft.Text(f"CONTATO: {contato_texto}", size=13, expand=True),
                ]),
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON, size=15, color=ft.Colors.GREY_700),
                    ft.Text(f"ORIGEM: {origem_texto}", size=13, expand=True),
                    ft.Icon(ft.Icons.STRAIGHTEN, size=15, color=ft.Colors.GREY_700),
                    ft.Text(f"DESTINO: {destino_texto}", size=13, expand=True),
                    ft.Icon(ft.Icons.LOCATION_ON, size=15, color=ft.Colors.GREY_700),
                    ft.Text(f"DIMENSÕES: {dimensoes_texto}", size=13, expand=True),
                    ft.Icon(ft.Icons.FITNESS_CENTER, size=15, color=ft.Colors.GREY_700),
                    ft.Text(f"PESO: {peso_texto}", size=13),
                ]),
            ])
            list_view.controls.append(
                ft.Container(
                    content=card_content,
                    bgcolor=ft.Colors.GREY_300,
                    padding=10,
                    border_radius=8
                )
            )
        page.update()


    def acrescentarNovo(e):
        if not input_projeto.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("O nome do projeto é obrigatório!"))
            page.snack_bar.open = True
            page.update()
            return

        hoje = datetime.now().strftime("%d/%m/%Y")
        cliente = input_cliente.value.strip() if input_cliente.value else None
        projeto = input_projeto.value.strip()
        so = input_so.value.strip() if input_so.value else None
        urgencia = 0 if dropdown_urgencia.value == "Baixa" else 1
        modal = dropdown_modal.value if dropdown_modal.value else None
        descricao = input_descricao.value.strip() if input_descricao.value else None
        prazo = input_prazo.value if input_prazo.value else None
        contato = input_contato.value.strip() if input_contato.value else None
        origem = input_origem.value.strip() if input_origem.value else None
        destino = input_destino.value.strip() if input_destino.value else None
        dimensoes = input_dimensoes.value.strip() if input_dimensoes.value else None
        peso = input_peso.value.strip() if input_peso.value else None
        observacao = input_observacao.value.strip() if input_observacao.value else None
        followup = input_followup.value.strip() if input_followup.value else None

        db.inserir_cotacao(
            data_registro=hoje,
            cliente=cliente,
            projeto=projeto,
            so=so,
            urgencia=urgencia,
            modal=modal,
            descricao=descricao,
            prazo_final=prazo,
            contato=contato,
            origem=origem,
            destino=destino,
            dimensoes=dimensoes,
            peso=peso,
            observacao=observacao,
            followup=followup
        )

        input_cliente.value = ""
        input_projeto.value = ""
        input_so.value = ""
        dropdown_urgencia.value = "Baixa"
        dropdown_modal.value = None
        input_descricao.value = ""
        input_prazo.value = ""
        input_contato.value = ""
        input_origem.value = ""
        input_destino.value = ""
        input_dimensoes.value = ""
        input_peso.value = ""
        input_observacao.value = ""
        input_followup.value = ""

        renderizar_tudo()


    def deletar(cotacao_id):
        db.deletar_cotacao(cotacao_id)
        renderizar_tudo()


    def abrirModalEdicao(cotacao_id):
        cotacoes = db.listar_cotacoes()
        cotacao = next((t for t in cotacoes if t[0] == cotacao_id), None)

        if not cotacao:
            page.snack_bar = ft.SnackBar(ft.Text("Cotação não encontrada!"))
            page.snack_bar.open = True
            page.update()
            return

        (u_id, _data_registro, u_cliente, u_projeto, u_so, u_urgencia, u_modal,
         u_descricao, u_prazo_final, u_contato, u_origem, u_destino, u_dimensoes,
         u_peso, u_observacao, u_followup) = cotacao

        edit_cliente = ft.TextField(value=u_cliente or "", label="CLIENTE", width=300)
        edit_projeto = ft.TextField(value=u_projeto, label="PROJETO")
        edit_so = ft.TextField(value=u_so or "", label="S.O.")
        edit_urgencia = ft.Dropdown(
            label="Urgência",
            value="Baixa" if u_urgencia == 0 else "Alta",
            options=[ft.dropdown.Option("Baixa"), ft.dropdown.Option("Alta")],
            width=150
        )
        edit_modal = ft.Dropdown(
            label="MODAL",
            value=u_modal,
            options=[
                ft.dropdown.Option("rodoviário"),
                ft.dropdown.Option("ferroviário"),
                ft.dropdown.Option("marítimo"),
                ft.dropdown.Option("fluvial"),
                ft.dropdown.Option("aéreo"),
                ft.dropdown.Option("multimodal")
            ],
            width=200
        )
        edit_descricao = ft.TextField(value=u_descricao, label="DESCRIÇÃO")
        edit_prazo = ft.TextField(value=u_prazo_final or "", label="PRAZO (DD/MM/AAAA)")
        edit_contato = ft.TextField(value=u_contato or "", label="CONTATO", width=450)
        edit_origem = ft.TextField(value=u_origem or "", label="ORIGEM", width=300)
        edit_destino = ft.TextField(value=u_destino or "", label="DESTINO", width=300)
        edit_dimensoes = ft.TextField(value=u_dimensoes or "", label="DIMENSÕES | mm | (PEÇA)", width=600)
        edit_peso = ft.TextField(value=u_peso or "", label="PESO (kg)", width=200)
        edit_observacao = ft.TextField(value=u_observacao or "", label="OBSERVAÇÃO", width=1030)
        edit_followup = ft.TextField(value=u_followup or "", label="FOLLOW-UP", expand=True, multiline=True, min_lines=2, max_lines=3)


        def fechar_modal(e=None):
            modal.open = False
            page.update()


        def save_edit(e):
            if not edit_projeto.value or not edit_projeto.value.strip():
                page.snack_bar = ft.SnackBar(ft.Text("Nome do projeto obrigatório!"))
                page.snack_bar.open = True
                page.update()
                return

            cliente_val = edit_cliente.value.strip() if edit_cliente.value else None
            projeto_val = edit_projeto.value.strip()
            so_val = edit_so.value.strip() if edit_so.value else None
            urgencia_val = 0 if edit_urgencia.value == "Baixa" else 1
            modal_val = edit_modal.value
            descricao_val = edit_descricao.value.strip() if edit_descricao.value else None
            prazo_final = edit_prazo.value.strip() if edit_prazo.value else None
            contato_val = edit_contato.value.strip() if edit_contato.value else None
            origem_val = edit_origem.value.strip() if edit_origem.value else None
            destino_val = edit_destino.value.strip() if edit_destino.value else None
            dimensoes_val = edit_dimensoes.value.strip() if edit_dimensoes.value else None
            peso_val = edit_peso.value.strip() if edit_peso.value else None
            observacao_val = edit_observacao.value.strip() if edit_observacao.value else None
            followup_val = edit_followup.value.strip() if edit_followup.value else None

            db.atualizar_cotacao(
                cotacao_id=u_id,
                cliente=cliente_val,
                projeto=projeto_val,
                so=so_val,
                urgencia=urgencia_val,
                modal=modal_val,
                descricao=descricao_val,
                prazo_final=prazo_final,
                contato=contato_val,
                origem=origem_val,
                destino=destino_val,
                dimensoes=dimensoes_val,
                peso=peso_val,
                observacao=observacao_val,
                followup=followup_val
            )
            fechar_modal()
            renderizar_tudo()


        modal = ft.AlertDialog(
            title=ft.Text("EDITAR REGISTRO"),
            content=ft.Column([
                ft.Row([edit_cliente, edit_projeto, edit_so, edit_urgencia], spacing=5),
                ft.Row([edit_modal, edit_descricao, edit_prazo], spacing=5),
                ft.Row([edit_contato, edit_origem, edit_destino], spacing=5),
                ft.Row([edit_dimensoes, edit_peso], spacing=5),
                ft.Row([edit_observacao], spacing=5),
                ft.Row([edit_followup], spacing=5),
            ], tight=True, spacing=10, scroll=ft.ScrollMode.ALWAYS),
            actions=[
                ft.TextButton("Salvar", on_click=save_edit),
                ft.TextButton("Cancelar", on_click=fechar_modal)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()


    # --- INTERFACE DE CRIAÇÃO ---

    input_cliente = ft.TextField(label="CLIENTE", width=300, max_length=30)
    input_projeto = ft.TextField(label="PROJETO", width=400, max_length=40)
    input_so = ft.TextField(label="S.O.", hint_text="0000.0000", width=200, max_length=12)

    dropdown_urgencia = ft.Dropdown(
        label="Urgência",
        value="Baixa",
        options=[ft.dropdown.Option("Baixa"), ft.dropdown.Option("Alta")],
        width=120
    )
    dropdown_modal = ft.Dropdown(
        label="MODAL",
        hint_text="Selecione o modal",
        options=[
            ft.dropdown.Option("rodoviário"),
            ft.dropdown.Option("ferroviário"),
            ft.dropdown.Option("marítimo"),
            ft.dropdown.Option("fluvial"),
            ft.dropdown.Option("aéreo"),
            ft.dropdown.Option("multimodal")
        ],
        width=200,
    )
    input_descricao = ft.TextField(label="DESCRIÇÃO", width=500, max_length=50)
    input_prazo = ft.TextField(label="PRAZO FINAL", width=150, read_only=True)
    input_contato = ft.TextField(label="CONTATO", width=540, max_length=50, hint_text="Nome / Telefone / email")
    input_origem = ft.TextField(label="ORIGEM", width=300, max_length=30)
    input_destino = ft.TextField(label="DESTINO", width=300, max_length=30)
    input_dimensoes = ft.TextField(label="DIMENSÕES | mm | (PEÇA)", width=410, max_length=40, hint_text="COMPR x LARG x ALT (PEÇA)")
    input_peso = ft.TextField(label="PESO (kg)", width=220, max_length=20)
    input_observacao = ft.TextField(label="OBSERVAÇÃO", width=1030, max_length=125)
    input_followup = ft.TextField(label="FOLLOW-UP", expand=True, multiline=True, min_lines=2, max_lines=2, max_length=2000)

    btn_calendario = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=abrir_calendario)
    btn_add = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=acrescentarNovo)



    # FILTROS

    input_busca_projeto = ft.TextField(
        label="Buscar por PROJETO",
        width=200,
        hint_text="Digite o nome do projeto",
        on_change=buscarPor_projeto,
        prefix_icon=ft.Icons.SEARCH,
        fill_color=ft.Colors.GREY_200
    )
    input_busca_so = ft.TextField(
        label="Buscar por S.O.",
        width=180,
        hint_text="Nº do S.O.",
        on_change=buscarPor_so,
        prefix_icon=ft.Icons.SEARCH,
        fill_color=ft.Colors.GREY_200
    )
    input_busca_cliente = ft.TextField(
        label="Buscar por CLIENTE",
        width=200,
        hint_text="Digite o nome do cliente",
        on_change=buscarPor_cliente,
        prefix_icon=ft.Icons.SEARCH,
        fill_color=ft.Colors.GREY_200
    )
    btn_limpar_filtros = ft.Button(
        "Limpar Filtros",
        icon=ft.Icons.CLEAR,
        on_click=limpar_filtros,
        bgcolor=ft.Colors.BLUE_GREY_100
    )

    btn_ordenar_cliente = ft.IconButton(
        icon=ft.Icons.SORT,
        tooltip="Ordenar por cliente (A-Z)",
        on_click=alternar_ordenacao_cliente,
        icon_color=ft.Colors.BLUE_ACCENT,
    )

    btn_ordenar_prazo = ft.IconButton(
        icon=ft.Icons.SORT,
        tooltip="Ordenar por prazo final",
        on_click=alternar_ordenacao_prazo,
        icon_color=ft.Colors.BLUE_ACCENT,
    )

    btn_ordenar_urgencia = ft.IconButton(
        icon=ft.Icons.SORT,
        tooltip="Ordenar por urgência (Alta primeiro)",
        on_click=alternar_ordenacao_urgencia,
        icon_color=ft.Colors.BLUE_ACCENT,
    )

    
    # BOTÃO DE BACKUP
    
    btn_backup = ft.IconButton(
        icon=ft.Icons.BACKUP,
        tooltip="Fazer backup do banco de dados no Desktop",
        on_click=fazer_backup,
        icon_color=ft.Colors.GREEN,
    )


    # LAYOUT

    page.add(
        ft.Text("GERENCIADOR DE COTAÇÕES", size=20, weight="bold"),
        ft.Divider(),
        ft.Row([input_cliente, input_projeto, input_so, dropdown_urgencia, dropdown_modal]),
        ft.Row([input_descricao, input_prazo, btn_calendario, input_contato]),
        ft.Row([input_origem, input_destino, input_dimensoes, input_peso]),
        ft.Row([input_observacao]),
        ft.Row([input_followup, btn_add]),
        ft.Divider(),
        ft.Row([input_busca_cliente, input_busca_projeto, input_busca_so, btn_limpar_filtros, btn_ordenar_cliente,
                 btn_ordenar_prazo, btn_ordenar_urgencia, btn_backup]),
        ft.Divider(),
        list_view
    )

    renderizar_tudo()

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")