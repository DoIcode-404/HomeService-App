import 'package:client/data/constants/constants.dart';
import 'package:flutter/material.dart';

class QuantityCard extends StatefulWidget {
  final String text;
  final void Function(int) onChanged;

  const QuantityCard({super.key, required this.text, required this.onChanged});

  @override
  QuantityCardState createState() => QuantityCardState();
}

class QuantityCardState extends State<QuantityCard> {
  int quantity = 0;

  void increment() {
    setState(() {
      quantity++;
      widget.onChanged(quantity);
    });
  }

  void decrement() {
    setState(() {
      if (quantity > 0) {
        quantity--;
        widget.onChanged(quantity);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(widget.text, style: AppTypography.kLight16),
        const Spacer(),
        QuantityActionButton(onTap: decrement, icon: Icons.remove),
        SizedBox(width: 17),
        Text(quantity.toString(), style: AppTypography.kExtraLight18),
        SizedBox(width: 17),
        QuantityActionButton(
          onTap: increment,
          icon: Icons.add,
          isActive: quantity > 0,
        ),
      ],
    );
  }
}

class QuantityActionButton extends StatelessWidget {
  final VoidCallback onTap;
  final IconData icon;
  final bool isActive;

  const QuantityActionButton({
    super.key,
    required this.onTap,
    required this.icon,
    this.isActive = false,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        height: 36,
        width: 36,
        decoration: BoxDecoration(
          color: isActive ? AppColors.kPrimary : null,
          border: isActive ? null : Border.all(color: AppColors.kHint),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Icon(
          icon,
          size: 20,
          color: isActive ? AppColors.kWhite : AppColors.kHint,
        ),
      ),
    );
  }
}
