import flet as ft
from datetime import datetime
from database import Database

def main(page: ft.Page):
    db = Database()
    page.title = "GERENCIADOR DE COTAÇÕES | Criado por ROBSON BEZERRA | robsonb0819@gmail.com"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = ft.ScrollMode.ALWAYS  # Scroll na página principal
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_color=ft.Colors.BLUE_ACCENT,
            thickness=8,
            main_axis_margin=5,
            thumb_visibility=True
        )
    )

    # FUNÇÃO PARA FAZER BACKUP
    def fazer_backup(e):
        sucesso, mensagem = db.backup()
        print(f"BACKUP - Sucesso: {sucesso}, Mensagem: {mensagem}")
        page.snack_bar = ft.SnackBar(
            ft.Text(mensagem),
            bgcolor=ft.Colors.GREEN if sucesso else ft.Colors.RED,
            duration=5000
        )
        page.snack_bar.open = True
        page.update()

    # CONTAINER PARA LISTAGEM (responsivo)
    list_container = ft.Column(spacing=10, scroll=ft.ScrollMode.ALWAYS, expand=True)

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

    def abrir_calendario(e): 
        pegarData.open = True
        page.update()

    def converter_data(data_str):
        if not data_str:
            return None
        try:
            return datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            return None
    
    def renderizar_tudo():
        list_container.controls.clear()
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

            # Card responsivo usando Column
            card_content = ft.Column([
                # Linha 1: Cliente, Projeto, Data
                ft.ResponsiveRow([
                    ft.Column([ft.Row([ft.Icon(ft.Icons.PERSON, size=16), ft.Text(f"CLIENTE: {cliente_texto}", size=14, weight="bold")])], col={"xs": 12, "sm": 6, "md": 4}),
                    ft.Column([ft.Row([ft.Icon(ft.Icons.BUSINESS, size=16), ft.Text(f"PROJETO: {projeto}", size=14, weight="bold")])], col={"xs": 12, "sm": 6, "md": 5}),
                    ft.Column([ft.Row([ft.Icon(ft.Icons.CALENDAR_TODAY, size=14), ft.Text(f"REG: {data_registro}", size=12)]), 
                              ft.Row([ft.IconButton(ft.Icons.EDIT, on_click=lambda e, tid=cotacao_id: abrirModalEdicao(tid), icon_size=18),
                                    ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, tid=cotacao_id: deletar(tid), icon_size=18)])], col={"xs": 12, "sm": 12, "md": 3}),
                ], spacing=5),
                
                # Linha 2: Prazo, Urgência, Descrição, SO, Modal
                ft.ResponsiveRow([
                    ft.Column([ft.Row([ft.Icon(ft.Icons.EVENT_AVAILABLE, size=14, color=urg_color), ft.Text(f"PRAZO: {prazo_texto}", size=12)])], col={"xs": 12, "sm": 6, "md": 2}),
                    ft.Column([ft.Text(f"URGÊNCIA: {urg_texto}", size=12, color=urg_color)], col={"xs": 12, "sm": 6, "md": 1}),
                    ft.Column([ft.Text(f"DESCRIÇÃO: {descricao}", size=12)], col={"xs": 12, "sm": 12, "md": 5}),
                    ft.Column([ft.Row([ft.Icon(ft.Icons.ASSIGNMENT_LATE, size=14), ft.Text(f"S.O.: {so_texto}", size=12, italic=True)])], col={"xs": 12, "sm": 6, "md": 2}),
                    ft.Column([ft.Row([ft.Icon(modal_icon, size=14), ft.Text(f"{modal_texto.capitalize()}", size=12)])], col={"xs": 12, "sm": 6, "md": 2}),
                ], spacing=5),
                
                # Observação
                ft.Row([ft.Icon(ft.Icons.NOTES, size=14), ft.Text(f"OBS: {observacao_texto}", size=12)]),
                
                # Follow-up
                ft.Container(
                    height=60,
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[ft.Text(f"FOLLOW-UP:\n{followup_texto}", size=12)]
                    ),
                    border=ft.Border.all(0.5, ft.Colors.GREY_500),
                    padding=5,
                ),
                
                # Contato, Origem, Destino, Dimensões, Peso
                ft.ResponsiveRow([
                    ft.Column([ft.Row([ft.Icon(ft.Icons.PERSON, size=12), ft.Text(f"CONTATO: {contato_texto}", size=11)])], col={"xs": 12, "sm": 6, "md": 3}),
                    ft.Column([ft.Row([ft.Icon(ft.Icons.LOCATION_ON, size=12), ft.Text(f"ORIGEM: {origem_texto}", size=11)])], col={"xs": 12, "sm": 6, "md": 2}),
                    ft.Column([ft.Row([ft.Icon(ft.Icons.STRAIGHTEN, size=12), ft.Text(f"DESTINO: {destino_texto}", size=11)])], col={"xs": 12, "sm": 6, "md": 2}),
                    ft.Column([ft.Row([ft.Icon(ft.Icons.LOCATION_ON, size=12), ft.Text(f"DIMENSÕES: {dimensoes_texto}", size=11)])], col={"xs": 12, "sm": 6, "md": 3}),
                    ft.Column([ft.Row([ft.Icon(ft.Icons.FITNESS_CENTER, size=12), ft.Text(f"PESO: {peso_texto}", size=11)])], col={"xs": 12, "sm": 6, "md": 2}),
                ], spacing=5),
            ])
            
            list_container.controls.append(
                ft.Container(
                    content=card_content,
                    bgcolor=ft.Colors.GREY_100,
                    padding=8,
                    border_radius=8,
                    margin=ft.Margin.only(bottom=5)
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

        edit_cliente = ft.TextField(value=u_cliente or "", label="CLIENTE", expand=True)
        edit_projeto = ft.TextField(value=u_projeto, label="PROJETO", expand=True)
        edit_so = ft.TextField(value=u_so or "", label="S.O.", expand=True)
        edit_urgencia = ft.Dropdown(
            label="Urgência",
            value="Baixa" if u_urgencia == 0 else "Alta",
            options=[ft.dropdown.Option("Baixa"), ft.dropdown.Option("Alta")],
            expand=True
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
            expand=True
        )
        edit_descricao = ft.TextField(value=u_descricao, label="DESCRIÇÃO", expand=True)
        edit_prazo = ft.TextField(value=u_prazo_final or "", label="PRAZO (DD/MM/AAAA)", expand=True)
        edit_contato = ft.TextField(value=u_contato or "", label="CONTATO", expand=True)
        edit_origem = ft.TextField(value=u_origem or "", label="ORIGEM", expand=True)
        edit_destino = ft.TextField(value=u_destino or "", label="DESTINO", expand=True)
        edit_dimensoes = ft.TextField(value=u_dimensoes or "", label="DIMENSÕES | mm | (PEÇA)", expand=True)
        edit_peso = ft.TextField(value=u_peso or "", label="PESO (kg)", expand=True)
        edit_observacao = ft.TextField(value=u_observacao or "", label="OBSERVAÇÃO", expand=True)
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

        # Modal responsivo
        modal = ft.AlertDialog(
            title=ft.Text("EDITAR REGISTRO"),
            content=ft.Container(
                content=ft.Column([
                    ft.ResponsiveRow([
                        ft.Column([edit_cliente], col={"xs": 12, "sm": 6, "md": 4}),
                        ft.Column([edit_projeto], col={"xs": 12, "sm": 6, "md": 4}),
                        ft.Column([edit_so], col={"xs": 12, "sm": 12, "md": 4}),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column([edit_urgencia], col={"xs": 12, "sm": 6, "md": 4}),
                        ft.Column([edit_modal], col={"xs": 12, "sm": 6, "md": 4}),
                        ft.Column([edit_descricao], col={"xs": 12, "sm": 12, "md": 4}),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column([edit_prazo], col={"xs": 12, "sm": 6, "md": 6}),
                        ft.Column([edit_contato], col={"xs": 12, "sm": 6, "md": 6}),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column([edit_origem], col={"xs": 12, "sm": 6, "md": 4}),
                        ft.Column([edit_destino], col={"xs": 12, "sm": 6, "md": 4}),
                        ft.Column([edit_dimensoes], col={"xs": 12, "sm": 12, "md": 6}),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column([edit_peso], col={"xs": 12, "sm": 6, "md": 6}),
                        ft.Column([edit_observacao], col={"xs": 12, "sm": 6, "md": 6}),
                    ]),
                    ft.Column([edit_followup]),
                ], spacing=10, scroll=ft.ScrollMode.ALWAYS),
                width=800,
                height=500,
            ),
            actions=[
                ft.TextButton("Salvar", on_click=save_edit),
                ft.TextButton("Cancelar", on_click=fechar_modal)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(modal)
        modal.open = True
        page.update()

    # --- INTERFACE DE CRIAÇÃO (Responsiva) ---
    input_cliente = ft.TextField(label="CLIENTE", expand=True, max_length=30)
    input_projeto = ft.TextField(label="PROJETO", expand=True, max_length=40)
    input_so = ft.TextField(label="S.O.", hint_text="0000.0000", expand=True, max_length=12)

    dropdown_urgencia = ft.Dropdown(
        label="Urgência",
        value="Baixa",
        options=[ft.dropdown.Option("Baixa"), ft.dropdown.Option("Alta")],
        expand=True
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
        expand=True,
    )
    input_descricao = ft.TextField(label="DESCRIÇÃO", expand=True, max_length=50)
    input_prazo = ft.TextField(label="PRAZO FINAL", expand=True, read_only=True)
    input_contato = ft.TextField(label="CONTATO", expand=True, max_length=50, hint_text="Nome / Telefone / email")
    input_origem = ft.TextField(label="ORIGEM", expand=True, max_length=30)
    input_destino = ft.TextField(label="DESTINO", expand=True, max_length=30)
    input_dimensoes = ft.TextField(label="DIMENSÕES | mm | (PEÇA)", expand=True, max_length=40, hint_text="COMPR x LARG x ALT (PEÇA)")
    input_peso = ft.TextField(label="PESO (kg)", expand=True, max_length=20)
    input_observacao = ft.TextField(label="OBSERVAÇÃO", expand=True, max_length=125)
    input_followup = ft.TextField(label="FOLLOW-UP", expand=True, multiline=True, min_lines=2, max_lines=2, max_length=2000)

    btn_calendario = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=abrir_calendario)
    btn_add = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=acrescentarNovo)

    # FILTROS (Responsivos)
    input_busca_projeto = ft.TextField(
        label="Buscar PROJETO",
        hint_text="Digite o nome",
        on_change=buscarPor_projeto,
        prefix_icon=ft.Icons.SEARCH,
        fill_color=ft.Colors.GREY_200,
        expand=True
    )
    input_busca_so = ft.TextField(
        label="Buscar S.O.",
        hint_text="Nº do S.O.",
        on_change=buscarPor_so,
        prefix_icon=ft.Icons.SEARCH,
        fill_color=ft.Colors.GREY_200,
        expand=True
    )
    input_busca_cliente = ft.TextField(
        label="Buscar CLIENTE",
        hint_text="Digite o nome",
        on_change=buscarPor_cliente,
        prefix_icon=ft.Icons.SEARCH,
        fill_color=ft.Colors.GREY_200,
        expand=True
    )
    btn_limpar_filtros = ft.Button(
        "Limpar",
        icon=ft.Icons.CLEAR,
        on_click=limpar_filtros,
        bgcolor=ft.Colors.BLUE_GREY_100,
        expand=True
    )

    btn_ordenar_cliente = ft.IconButton(
        icon=ft.Icons.SORT,
        tooltip="Ordenar por cliente",
        on_click=alternar_ordenacao_cliente,
        icon_color=ft.Colors.BLUE_ACCENT,
    )

    btn_ordenar_prazo = ft.IconButton(
        icon=ft.Icons.SORT,
        tooltip="Ordenar por prazo",
        on_click=alternar_ordenacao_prazo,
        icon_color=ft.Colors.BLUE_ACCENT,
    )

    btn_ordenar_urgencia = ft.IconButton(
        icon=ft.Icons.SORT,
        tooltip="Ordenar por urgência",
        on_click=alternar_ordenacao_urgencia,
        icon_color=ft.Colors.BLUE_ACCENT,
    )
    
    btn_backup = ft.IconButton(
        icon=ft.Icons.BACKUP,
        tooltip="Fazer backup",
        on_click=fazer_backup,
        icon_color=ft.Colors.GREEN,
    )

    # LAYOUT PRINCIPAL (Totalmente responsivo)
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("GERENCIADOR DE COTAÇÕES", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                
                # Formulário de cadastro responsivo
                ft.ResponsiveRow([
                    ft.Column([input_cliente], col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
                    ft.Column([input_projeto], col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
                    ft.Column([input_so], col={"xs": 12, "sm": 6, "md": 4, "lg": 2}),
                    ft.Column([dropdown_urgencia], col={"xs": 12, "sm": 6, "md": 4, "lg": 2}),
                    ft.Column([dropdown_modal], col={"xs": 12, "sm": 12, "md": 12, "lg": 2}),
                ], spacing=8),
                
                ft.ResponsiveRow([
                    ft.Column([input_descricao], col={"xs": 12, "sm": 8, "md": 8, "lg": 8}),
                    ft.Column([ft.Row([input_prazo, btn_calendario], spacing=5)], col={"xs": 12, "sm": 4, "md": 4, "lg": 4}),
                ], spacing=8),
                
                ft.ResponsiveRow([
                    ft.Column([input_contato], col={"xs": 12, "sm": 6, "md": 4, "lg": 4}),
                    ft.Column([input_origem], col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
                    ft.Column([input_destino], col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
                    ft.Column([input_dimensoes], col={"xs": 12, "sm": 6, "md": 4, "lg": 2}),
                ], spacing=8),
                
                ft.ResponsiveRow([
                    ft.Column([input_peso], col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
                    ft.Column([input_observacao], col={"xs": 12, "sm": 6, "md": 8, "lg": 9}),
                ], spacing=8),
                
                ft.Row([input_followup, btn_add], spacing=5),
                ft.Divider(),
                
                # Filtros responsivos
                ft.ResponsiveRow([
                    ft.Column([input_busca_cliente], col={"xs": 12, "sm": 12, "md": 4}),
                    ft.Column([input_busca_projeto], col={"xs": 12, "sm": 6, "md": 3}),
                    ft.Column([input_busca_so], col={"xs": 12, "sm": 6, "md": 3}),
                    ft.Column([btn_limpar_filtros], col={"xs": 12, "sm": 12, "md": 2}),
                ], spacing=5),
                
                ft.Row([btn_ordenar_cliente, btn_ordenar_prazo, btn_ordenar_urgencia, btn_backup], spacing=5),
                ft.Divider(),
                
                # Listagem responsiva
                ft.Container(content=list_container, expand=True),
            ], spacing=10),
            expand=True,
            padding=10
        )
    )

    renderizar_tudo()

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")