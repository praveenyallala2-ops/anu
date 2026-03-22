# 👮 Automated Police Duty Roster System

An automated solution for managing police personnel and generating daily duty rosters (shifts). This system simplifies administrative tasks by providing a one-click automated scheduling feature and professional PDF reporting.

## 🚀 Features

- **Staff Management**: Add, view, edit, and delete police personnel with contact details.
- **Automated Scheduling**: Automatically assigns staff to Morning, Evening, and Night shifts.
- **PDF Export**: Generate and download professional duty charts as PDFs.
- **Dark Mode Dashboard**: Modern, clean, and professional user interface.
- **Persistent Storage**: Uses SQLite for seamless data management.

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, Flask
- **Database**: SQLite
- **PDF Generation**: ReportLab
- **Frontend**: HTML5, Vanilla CSS

## 📋 Prerequisites

Ensure you have Python installed. You will also need to install the following dependencies:

```bash
pip install flask reportlab
```

## 🏃 How to Run

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/praveenyallala2-ops/anu.git
    cd anu
    ```
2.  **Run the application**:
    ```bash
    python app.py
    ```
3.  **Access the dashboard**:
    Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

## 📂 Project Structure

- `app.py`: Main application logic and database management.
- `database.db`: SQLite database file.
- `templates/`: HTML templates (Dashboard, Staff management, etc.).
- `static/`: CSS styles and static assets.
- `Abstract.docx`: Project documentation.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
