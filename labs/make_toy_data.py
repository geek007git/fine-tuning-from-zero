"""Generate fictional group-separated ticket records for teaching only."""
import json
from pathlib import Path

SAMPLES = {
    "billing": [
        "My invoice shows a charge twice for the same month",
        "Please explain the unexpected subscription fee on my statement",
        "The receipt has the wrong tax amount",
        "I need a copy of the payment invoice for last week",
        "The refund for my duplicate card payment is missing",
        "Why did my annual plan renew at a higher price",
        "My bank shows two transactions for one order",
        "Where can I download the receipt for my purchase",
        "The discount was not applied to my final bill",
        "I cancelled but a new charge appeared on my card",
        "The renewal amount on my account seems incorrect",
        "Please correct the billing address printed on the invoice",
        "The payment succeeded but the invoice still says unpaid",
        "Can you explain this extra processing fee",
        "I want to know when my refund will appear",
    ],
    "technical": [
        "The mobile app crashes whenever I open the camera",
        "Uploads freeze at ninety percent on my laptop",
        "The screen stays blank after the latest update",
        "Video playback stops after a few seconds",
        "The export button produces an empty file",
        "My browser shows an error when I save changes",
        "The Android app closes when I tap notifications",
        "Images are not loading on the dashboard",
        "The download link fails with a server error",
        "My microphone is not detected during a call",
        "The page becomes unresponsive after selecting a filter",
        "The filter never applies when I select it",
        "Search results disappear when I scroll",
        "The desktop program refuses to open after installation",
        "The chart does not refresh when I change the date",
    ],
    "account": [
        "I cannot sign in after resetting my password",
        "Please update the email address on my profile",
        "The verification code never arrives for my login",
        "How do I enable two factor authentication",
        "I lost access to the phone linked to my account",
        "Please change the display name in my profile",
        "My account was locked after several sign in attempts",
        "I need to remove an old device from my account",
        "The password reset link has expired",
        "I want to close my account and remove my profile",
        "My details appear under someone else's name",
        "The invitation does not give my teammate access",
        "Please help me recover my username",
        "I cannot change my account recovery email",
        "My security settings do not save after login",
    ],
}


def main():
    path = Path(__file__).parent / "data" / "toy_tickets.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for label, examples in SAMPLES.items():
        for index, ticket in enumerate(examples):
            split = ("train", "validation", "test")[index // 5]
            rows.append({"id": f"{label[:3]}-{index + 1:02d}",
                         "group": f"fictional-{label}-{index + 1:02d}",
                         "split": split, "text": ticket, "label": label})
    # Keep the tracked fixture byte-for-byte identical on Windows and Linux.
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} fictional tickets to {path}")


if __name__ == "__main__":
    main()
