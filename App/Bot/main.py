import asyncio

from telebot.asyncio_filters import ForwardFilter
from telebot.asyncio_filters import IsDigitFilter
from telebot.asyncio_filters import IsReplyFilter
from telebot.asyncio_filters import StateFilter

from App.Bot.Handlers.EditAccountActionsHandler import _sendAddAdvChatText
from App.Bot.Handlers.EditAccountActionsHandler import _sendChangeAccountMessageText
from App.Bot.Handlers.EditAccountActionsHandler import _sendChangePromptText
from App.Bot.Handlers.EditAccountActionsHandler import _sendChangeStatusMenu
from App.Bot.Handlers.EditAccountActionsHandler import _sendChangeTargetChannelText
from App.Bot.Handlers.EditAccountActionsHandler import _sendDeleteAccountText
from App.Bot.Handlers.EditAccountActionsHandler import _sendReloadChatGPTMessageText
from App.Bot.Handlers.EditAccountActionsHandler import _sendRemoveAdvChatText
from App.Bot.Handlers.EditAccountActionsHandler import _set_status_off
from App.Bot.Handlers.EditAccountActionsHandler import _set_status_on

from App.Bot.Handlers.ServiceMenuHandler import _serviceMenu

from App.Bot.Handlers.EditAccountVisualMenuHandler import _visualConfig
from App.Bot.Handlers.EditAccountVisualMenuHandler import _accountSessionsList
from App.Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeFirstNameText
from App.Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeLastNameText
from App.Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeUsernameText
from App.Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeProfilePictureText
from App.Bot.Handlers.EditAccountVisualActionsHandler import _sendChangeAccountDescriptionText

from App.Bot.Handlers.SpamTgHandler import _spamTg
from App.Bot.Handlers.SpamInstHandler import _spamInst

from App.Bot.Handlers.StoriesMenuHandler import _stories
from App.Bot.Handlers.StoriesActionsHandler import _sendAddTargetChatText
from App.Bot.Handlers.StoriesActionsHandler import _sendDeleteTargetChatText
from App.Bot.Handlers.StoriesActionsHandler import _launchStories

from App.Bot.Handlers.EditAccountsMenuHandler import _editAccountsMenu
from App.Bot.Handlers.EditAccountsMenuHandler import _showAccountActions
from App.Bot.Handlers.EditAccountsInstMenuHandler import _editAccountsInstMenu
from App.Bot.Handlers.EditAccountsInstMenuHandler import _showAccountInstActions

from App.Bot.Handlers.NewAccountHandler import _newAccountMenu
from App.Bot.Handlers.NewAccountInstHandler import _getInstAccountLogin

from App.Bot.Markups import MarkupBuilder  # noqa
from App.Bot.Middlewares import FloodingMiddleware
from App.Config import account_context
from App.Config import bot
from App.Config import message_context_manager
from App.Config import singleton
from App.Database.DAL.AccountTgDAL import AccountDAL
from App.Database.session import async_session
from App.Database.DAL.AccountInstDAL import AccountInstDAL



@singleton
class Bot:

    bot.add_custom_filter(StateFilter(bot))

    def __init__(self):
        bot.add_custom_filter(IsReplyFilter())
        bot.add_custom_filter(ForwardFilter())
        bot.add_custom_filter(IsDigitFilter())
        bot.setup_middleware(FloodingMiddleware(1))

    @staticmethod
    @bot.callback_query_handler(func=lambda call: True)
    async def HandlerInlineMiddleware(call):
        # ------------------menu----------------------

        if call.data == "back_to_service_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _serviceMenu(message=call.message)

        if call.data == "new_account_menu":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _newAccountMenu(call.message)

        if call.data == "spam_tg" or call.data == "back_to_spam_tg":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _spamTg(message=call.message)
        
        if call.data == "acc_edit" or call.data == "back_to_acc_edit":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _editAccountsMenu(message=call.message)
        
        if "edit_account" in call.data or "back_to_edit_menu" in call.data:
            await bot.delete_state(
                user_id=call.message.chat.id, chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _showAccountActions(message=call.message, account_name=account_name)

        if call.data == "vis_cfg": 
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _accountSessionsList(message=call.message)
        
        if call.data == "back_to_vis_cfg":
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            await _accountSessionsList(message=call.message)


        if "viscfg_account" in call.data or "back_to_viscfg_account" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            
            await _visualConfig(account_name=account_name, message=call.message)

        # ------------------stories------------------

        if call.data == "look_stories" or call.data == "back_to_stories":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            
            await _stories(message=call.message)
        

        # --------------stories actions--------------
        
        if call.data == "add_trgt_chnl":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _sendAddTargetChatText(message=call.message)
        
        if call.data == "delete_trgt_chnl":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _sendDeleteTargetChatText(message=call.message)
        
        if "stories_service" == call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
  
            await _launchStories(message=call.message)


        # -------editing visual account config-------
    
        if "chng_first_name" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeFirstNameText(message=call.message)

        if "chng_last_name" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeLastNameText(message=call.message)        
        
        if "chng_username" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeUsernameText(message=call.message)   
        
        if "chng_pfp" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeProfilePictureText(message=call.message)   
        
        if "chng_profile_desc" in call.data:
            for msgId in message_context_manager.help_menu_msgId_to_delete[call.message.chat.id]:
                await bot.delete_message(chat_id=call.message.chat.id, message_id=msgId)
            message_context_manager.help_menu_msgId_to_delete[call.message.chat.id] = None

            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id,
                account_name=account_name
            )
            await _sendChangeAccountDescriptionText(message=call.message)   

        # ---------------bot editing-----------------
            
        if "change_acc_msg" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendChangeAccountMessageText(call.message)

        if "change_prompt" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendChangePromptText(call.message)

        if "add_adv_chat" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendAddAdvChatText(call.message)

        if "remove_adv_chat" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendRemoveAdvChatText(call.message)

        if "change_target_channel" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )
            await _sendChangeTargetChannelText(call.message)

        if "change_status" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendChangeStatusMenu(call.message)

        if "reload_chatgpt_message" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendReloadChatGPTMessageText(call.message)

        if "delete_account" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _sendDeleteAccountText(call.message)

        if "set_status_on" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            async with async_session() as session:
                account_dal = AccountDAL(session)
                await account_dal.updateStatus(session_name=account_name, status=True)

            await _set_status_on(call.message)

        if "set_status_off" in call.data:
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            async with async_session() as session:
                account_dal = AccountDAL(session)
                await account_dal.updateStatus(session_name=account_name, status=False)

            await _set_status_off(call.message)

        # ---------------inst menu-----------------
        
        if call.data == "spam_inst" or call.data == "back_to_spam_inst":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _spamInst(message=call.message)

        if call.data == "logging_in_inst" or call.data == "back_to_logging_in_inst":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            await _getInstAccountLogin(message=call.message)
        
        if call.data == "inst_acc_edit" or call.data == "back_to_inst_acc_edit":
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )

            await _editAccountsInstMenu(message=call.message)

        if "edit_account_inst" in call.data:
            await message_context_manager.delete_msgId_from_help_menu_dict(
                chat_id=call.message.chat.id
            )
            account_name = call.data.split("#")[-1]
            account_context.updateAccountName(
                chat_id=call.message.chat.id, account_name=account_name
            )

            await _showAccountInstActions(message=call.message)
        


            
    @staticmethod
    async def polling():
        task1 = asyncio.create_task(bot.infinity_polling())
        await task1


if __name__ == "__main__":
    b = Bot()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(b.polling())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
