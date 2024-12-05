from typing import List
from langchain.schema import BaseMessage
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.lib import colors
import re

class ChatExporter:
    """
    A utility class to prepare and export user chat conversations.
    """

    def prepare_conversation_content(self, user_id: str, messages: List[BaseMessage]) -> str:
        """
        Prepares the conversation content as a well-formatted text string for download.

        Args:
            user_id (str): The unique identifier of the user whose conversation is being prepared.
            messages (List[BaseMessage]): A list of messages (HumanMessage, AIMessage, etc.).

        Returns:
            str: The prepared conversation content.

        Raises:
            ValueError: If the messages list is empty.
        """
        if not messages:
            raise ValueError("No messages to prepare for the given user.")

        formatted_content = [
            f"Chat Conversation with AI Assistant\nUser ID: {user_id}",
            f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "=" * 50,
        ]

        for message in messages:
            role = "User" if message.type == "human" else "Assistant"
            timestamp = getattr(message, "timestamp", None)
            formatted_timestamp = f" [{timestamp}]" if timestamp else ""
            formatted_content.append(f"{role}{formatted_timestamp}:\n{message.content.strip()}\n")
            formatted_content.append("-" * 50)

        return "\n".join(formatted_content)

    # def export_conversation_as_pdf(self, user_id: str, messages: List[BaseMessage]) -> str:
    #     """
    #     Exports the conversation as a PDF file.

    #     Args:
    #         user_id (str): The unique identifier of the user whose conversation is being prepared.
    #         messages (List[BaseMessage]): A list of messages (HumanMessage, AIMessage, etc.).

    #     Returns:
    #         str: The path to the generated PDF file.

    #     Raises:
    #         ValueError: If the messages list is empty.
    #     """
    #     if not messages:
    #         raise ValueError("No messages to prepare for the given user.")

    #     pdf_file_path = f"chat_{user_id}.pdf"
    #     pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=letter)
    #     pdf_canvas.setFont("Helvetica", 12)

    #     # Header
    #     y_position = 750
    #     pdf_canvas.drawString(50, y_position, f"Chat Conversation with AI Assistant")
    #     y_position -= 20
    #     pdf_canvas.drawString(50, y_position, f"User ID: {user_id}")
    #     y_position -= 20
    #     pdf_canvas.drawString(50, y_position, f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    #     y_position -= 30
    #     pdf_canvas.drawString(50, y_position, "=" * 70)
    #     y_position -= 20

    #     # Chat messages
    #     for message in messages:
    #         if y_position < 50:  # Check if space is running out
    #             pdf_canvas.showPage()
    #             pdf_canvas.setFont("Helvetica", 12)
    #             y_position = 750

    #         role = "User" if message.type == "human" else "Assistant"
    #         timestamp = getattr(message, "timestamp", None)
    #         formatted_timestamp = f" [{timestamp}]" if timestamp else ""
    #         pdf_canvas.drawString(50, y_position, f"{role}{formatted_timestamp}:")
    #         y_position -= 15

    #         # Break long message into multiple lines
    #         message_lines = self._split_message_into_lines(message.content.strip(), 80)
    #         for line in message_lines:
    #             pdf_canvas.drawString(70, y_position, line)
    #             y_position -= 15

    #         y_position -= 10  # Add space between messages

    #     pdf_canvas.save()
    #     return pdf_file_path
    
    def export_conversation_as_pdf(self, user_id: str, messages: List[BaseMessage]) -> str:
        """
        Exports the conversation as a PDF file with well-formatted content, including code blocks.

        Args:
            user_id (str): The unique identifier of the user whose conversation is being prepared.
            messages (List[BaseMessage]): A list of messages (HumanMessage, AIMessage, etc.).

        Returns:
            str: The path to the generated PDF file.

        Raises:
            ValueError: If the messages list is empty.
        """
        if not messages:
            raise ValueError("No messages to prepare for the given user.")

        pdf_file_path = f"chat_{user_id}.pdf"
        doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
        content = []

        # Styles
        header_style = ParagraphStyle(
            name="HeaderStyle",
            fontSize=14,
            leading=18,
            spaceAfter=10,
            textColor=colors.black,
            alignment=1  # Centered
        )
        normal_style = ParagraphStyle(
            name="NormalStyle",
            fontSize=12,
            leading=16,
            textColor=colors.black,
        )
        code_style = ParagraphStyle(
            name="CodeStyle",
            fontName="Courier",
            fontSize=10,
            leading=14,
            textColor=colors.blue,
            backColor=colors.whitesmoke,
            borderPadding=4,
            borderWidth=0.5,
            borderColor=colors.gray,
        )

        # Header
        content.append(Paragraph(f"Chat Conversation with AI Assistant", header_style))
        content.append(Paragraph(f"User ID: {user_id}", normal_style))
        content.append(Paragraph(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
        content.append(Paragraph("=" * 70, normal_style))

        # Chat messages
        for message in messages:
            role = "User" if message.type == "human" else "Assistant"
            content.append(Paragraph(f"<b>{role}:</b>", normal_style))

            # Handle message content
            message_content = message.content.strip()
            code_blocks = re.findall(r"```(.*?)```", message_content, re.DOTALL)

            if code_blocks:
                # Split message into non-code and code sections
                parts = re.split(r"```.*?```", message_content, flags=re.DOTALL)
                for i, part in enumerate(parts):
                    if part.strip():
                        content.append(Paragraph(part.strip(), normal_style))
                    if i < len(code_blocks):
                        code_block = code_blocks[i].strip()
                        content.append(Paragraph(f"<pre>{code_block}</pre>", code_style))
            else:
                content.append(Paragraph(message_content, normal_style))

            content.append(Paragraph("-" * 50, normal_style))  # Separator

        # Generate PDF
        doc.build(content)
        return pdf_file_path

    def _split_message_into_lines(self, message: str, line_length: int) -> List[str]:
        """
        Splits a long message into multiple lines of specified length.

        Args:
            message (str): The message to split.
            line_length (int): The maximum length of a single line.

        Returns:
            List[str]: The list of split lines.
        """
        words = message.split()
        lines, current_line = [], []
        for word in words:
            if len(" ".join(current_line + [word])) > line_length:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        lines.append(" ".join(current_line))
        return lines
