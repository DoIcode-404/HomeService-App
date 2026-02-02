import 'package:client/data/constants/constants.dart';
import 'package:client/modules/checkout/components/phone_number_card.dart';
import 'package:client/modules/home/components/search_field.dart';
import 'package:client/modules/widgets/buttons/custom_button.dart';
import 'package:client/modules/widgets/containers/primary_container.dart';
import 'package:client/modules/widgets/texts/custom_header_text.dart';
import 'package:flutter/material.dart';

class AddPhoneNumberView extends StatefulWidget {
  const AddPhoneNumberView({super.key});

  @override
  State<AddPhoneNumberView> createState() => _AddPhoneNumberViewState();
}

class _AddPhoneNumberViewState extends State<AddPhoneNumberView> {
  final _phoneNumberController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(leading: const BackButton()),
      body: SingleChildScrollView(
        padding: EdgeInsets.symmetric(horizontal: 20),
        child: Column(
          children: [
            SizedBox(height: 20),
            PrimaryContainer(
              child: Column(
                children: [
                  CustomHeaderText(text: 'Phone number', fontSize: 18),
                  SizedBox(height: 16),
                  SearchField(
                    controller: _phoneNumberController,
                    hintText: 'Phone Number',
                    isSearchField: false,
                    buttonText: 'Save',
                    onSearchPress: () {},
                  ),
                ],
              ),
            ),
            SizedBox(height: 20),
            PrimaryContainer(
              child: Column(
                children: [
                  Row(
                    children: [
                      CustomHeaderText(text: 'Phone Number', fontSize: 18),
                      const Spacer(),
                      CustomButton(
                        text: 'Change',
                        icon: AppAssets.kEdit,
                        onTap: () {},
                        isBorder: true,
                      ),
                    ],
                  ),
                  SizedBox(height: 16),
                  const PhoneNumberCard(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
