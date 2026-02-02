import 'package:client/model/chat_model.dart';
import 'package:client/modules/support/components/chat_bubble.dart';
import 'package:client/modules/support/components/message_field.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class LiveChatView extends StatefulWidget {
  const LiveChatView({super.key});

  @override
  State<LiveChatView> createState() => _LiveChatViewState();
}

class _LiveChatViewState extends State<LiveChatView> {
  final TextEditingController _textEditingController = TextEditingController();
  bool _isExpanded = false;

  @override
  void dispose() {
    _textEditingController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      appBar: AppBar(leading: const BackButton()),
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          children: [
            Row(
              children: [
                CustomHeaderText(text: 'Live Chat', fontSize: 18),
                const Spacer(),
                const Icon(Icons.more_horiz),
              ],
            ),
            SizedBox(height: 16),
            Expanded(
              child: ListView.separated(
                itemBuilder: (context, index) {
                  return ChatBubble(chat: dummyChats[index]);
                },
                separatorBuilder: (context, index) => SizedBox(height: 16),
                itemCount: dummyChats.length,
              ),
            ),
          ],
        ),
      ),
      bottomSheet: PrimaryContainer(
        radius: 0,
        child: MessageField(
          sendCallback: () {},
          attachmentCallback: () {},
          emojiCallback: () {},
          controller: _textEditingController,
          isExpanded: _isExpanded,
          onChanged: (value) {
            setState(() {
              _isExpanded = value.length > 13;
            });
          },
        ),
      ),
    );
  }
}
