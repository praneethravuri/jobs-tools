# 🚀 Job Search Automation Toolkit

A comprehensive, well-organized collection of tools to supercharge your job search. Features automated LinkedIn outreach, AI-powered email campaigns, resume management, and H1B visa sponsorship research.

## 📁 Project Structure

```
jobs-tools/
├── src/
│   ├── email/
│   │   ├── ai_generated/        # AI-powered personalized emails
│   │   └── cold_outreach/       # Cold email campaigns
│   ├── linkedin/                # LinkedIn automation scripts
│   ├── resume/
│   │   ├── generator/           # Resume generation from JSON
│   │   └── organizer/           # Resume file organization
│   └── scraping/                # H1B company data scraper
├── pyproject.toml               # uv package configuration
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Getting Started

### Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Environment Setup

Create a `.env` file in the project root:

```bash
GMAIL_APP_PASSWORD=your_gmail_app_password
EMAIL_FROM=your_email@gmail.com
```

---

## 📧 Email Outreach

### AI-Generated Personalized Emails

**Location:** `src/email/ai_generated/`

Leverage local AI models (via Ollama) to generate personalized, professional outreach emails at scale.

#### `generate_emails.py`
Generates customized emails for multiple recipients and saves them as JSON files organized by company.

```bash
python src/email/ai_generated/generate_emails.py
```

#### `send_emails.py`
Sends AI-generated emails with personalized content to your contact list.

```bash
python src/email/ai_generated/send_emails.py
```

**Requirements:**
- Install [Ollama](https://ollama.ai) and download your preferred model (e.g., `phi3`)
- Set `GMAIL_APP_PASSWORD` in your `.env` file

### Cold Email Outreach

**Location:** `src/email/cold_outreach/`

Send targeted cold emails to recruiters and potential referrers.

#### `send_without_attachment.py`
Send plain text emails for quick, lightweight outreach.

```bash
python src/email/cold_outreach/send_without_attachment.py
```

#### `send_with_attachment.py`
Send emails with resume attachments for formal applications.

```bash
python src/email/cold_outreach/send_with_attachment.py
```

---

## 🔗 LinkedIn Automation

**Location:** `src/linkedin/`

Browser console scripts for automating LinkedIn networking tasks.

### `referral_single.js`
Send personalized connection requests or messages to individual profiles. Navigate to a LinkedIn profile, open DevTools console, and paste the script.

**Features:**
- Target recruiters or employees
- Customize messages with company name and job ID
- Quick, one-click messaging

### `referral_multiple.js`
Automated mass outreach to multiple profiles on a company page.

**Usage:**
1. Visit a company's LinkedIn page
2. Filter by location and position
3. Open DevTools console and paste the script
4. Set connection limits to manage outreach volume

**Tip:** Start with smaller batches (10-20) to avoid LinkedIn rate limits.

### `withdraw_connections.js`
Bulk withdraw pending connection requests to keep your network clean and professional.

**Usage:**
1. Navigate to LinkedIn → My Network → Manage sent requests
2. Open DevTools console
3. Paste and run the script

---

## 📄 Resume Tools

### Resume Generator

**Location:** `src/resume/generator/create_docx.py`

Generate professionally formatted `.docx` resumes from JSON data.

```bash
python src/resume/generator/create_docx.py
```

**Features:**
- Custom formatting with proper spacing and alignment
- Sections: Work Experience, Education, Skills, Projects
- Professional styling with Calibri font

### Resume Organizer

**Location:** `src/resume/organizer/save_resume.py`

Automatically organize tailored resumes by company and position.

```bash
python src/resume/organizer/save_resume.py
```

**What it does:**
- Creates folders named `CompanyName-Position`
- Copies your resume from Desktop to `~/Documents/saved-applications/`
- Maintains organized archive of all applications

---

## 🔍 H1B Visa Sponsorship Research

**Location:** `src/scraping/h1b_companies.py`

Scrape and download data about companies that sponsor H1B visas.

```bash
python src/scraping/h1b_companies.py
```

**Output:** Creates `companies.csv` with company names, locations, and H1B filing statistics.

---

## 📝 Best Practices & Tips

### Email Outreach
- Always test with a small batch before sending to large lists
- Personalize templates for each company/role
- Track response rates to optimize messaging
- Respect unsubscribe requests and email frequency limits

### LinkedIn Automation
- Use LinkedIn automation responsibly to avoid account restrictions
- Limit bulk actions to 20-30 connections per session
- Always personalize messages when possible
- Wait 24-48 hours between bulk automation sessions

### Resume Management
- Keep a master JSON file with all your experience
- Tailor bullet points for each application
- Maintain backups of all customized resumes
- Use consistent naming: `CompanyName-Position`

---

## ⚙️ Configuration Examples

### Email List Format (for AI-generated emails)

```python
email_list = [
    {
        'name': 'John Doe',
        'email': 'john@company.com',
        'company': 'TechCorp',
        'position': 'Software Engineer'
    },
]
```

### Resume JSON Structure

See `src/resume/generator/create_docx.py` for the expected JSON schema with sections for header, work_experience, education, skills, and projects.

---

## 🛠️ Development

### Adding New Tools

```bash
# Create a new module
mkdir -p src/your_module
touch src/your_module/your_script.py

# Add dependencies if needed
uv pip install new-package
```

### Running Tests

```bash
uv pip install -e ".[dev]"
pytest
```

---

## ⚠️ Important Notes

- **LinkedIn Automation:** Use at your own risk. LinkedIn's terms of service prohibit automation. These scripts are educational and should be used responsibly.
- **Email Sending:** Gmail has daily sending limits (typically 500 emails/day for regular accounts). Monitor your quota.
- **API Keys:** Never commit `.env` files or API keys to version control.
- **H1B Data:** Information scraped from h1bdata.info is for research purposes only.

---

## Connect With Me

- **LinkedIn:** [https://www.linkedin.com/in/prav25/](https://www.linkedin.com/in/prav25/)
- **Website:** [https://praneethravuri.com/](https://praneethravuri.com/)