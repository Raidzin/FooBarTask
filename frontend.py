import logging

from httpx import HTTPError, post
from nicegui import ui


with ui.image('https://w.forfun.com/fetch/c6/c61a531f93b5cef71e45e8c01ab28435.jpeg').style('width: 100vw; height: 100vh; margin: auto;'):

    with ui.page_sticky(position='top').classes(replace='w-full row items-center justify-start bg-dark opacity-40') as header:
        ui.label('FooBar').classes(replace='text-h4 text-weight-bolder opacity-100')

    with ui.footer(value=False).classes('justify-center bg-dark') as footer:
        with ui.row().classes('w-full items-center'):
            ui.label('made with')
            ui.link('NiceGUI', 'https://nicegui.io').classes('text-white')
            ui.label('by')
            ui.link('Raidzin', 'https://github.com/Raidzin/FooBarTask').classes('text-white')

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20).classes('opacity-40'):
        ui.button(on_click=footer.toggle).props('fab icon=contact_support').props('color=dark').classes(' opacity-100')

    with ui.row().classes('w-full mt-64 justify-center items-center').style('background-color: #00000000'):
        with ui.column():
            with ui.card().classes('backdrop-blur-sm q-pa-lg').style('background-color: #00000000; border-radius: 15px'):
                async def update_text(value):
                    try:
                        digits = [
                            int(element.strip())
                            for element in value.value.strip().split(',')
                        ]
                        digits = post(
                            'http://is_divisible_by_3535/is_divisible_by',
                            json={'values': digits},
                            timeout=60,
                        ).json()
                        text = ''
                        for digit in digits:
                            match digit:
                                case 3:
                                    text += ' foo'
                                case 5:
                                    text += ' bar'
                                case 35:
                                    text += ' foobar'
                        result.set_text(text)
                    except HTTPError as error:
                        logging.exception(error)
                        result.set_text('Проблемы с сетью...')
                    except ValueError as error:
                        logging.exception(error)
                        result.set_text('Не корректный ввод...')


                ui.label(
                    'Введите список целых чисел'
                ).classes(
                    'text-h4 text-wrap'
                )
                ui.textarea(
                    placeholder='через запятую',
                    on_change=update_text
                ).classes(
                    'w-full items-center text-center'
                ).props(
                    'autofocus autogrow input-class=text-white'
                )

                result = ui.label()

ui.query('div.nicegui-content').classes('nicegui-content q-pa-none bg-black')


ui.run(host='0.0.0.0', port=80, title='FooBar')
