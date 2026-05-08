# SAHMSEC – QVD-2026-14149 Weaver E-cology10 RCE Scanner

## Overview

This repository contains a Python-based Proof of Concept (PoC) script for testing the reported **QVD-2026-14149** vulnerability affecting **Weaver E-cology10** systems.

The vulnerability is described as an **Unauthenticated Remote Code Execution (RCE)** issue through a vulnerable Dubbo API debug endpoint.

> ⚠️ This project is provided strictly for:
>
> * Authorized security testing
> * Internal security validation
> * Educational and research purposes
>
> Unauthorized access or testing against systems you do not own or explicitly have permission to assess is illegal.

---

## Vulnerability Information

| Field              | Value                                 |
| ------------------ | ------------------------------------- |
| Vulnerability ID   | QVD-2026-14149                        |
| Product            | Weaver E-cology10                     |
| Vulnerability Type | Unauthenticated Remote Code Execution |
| Severity           | Critical                              |
| CVSS               | 9.8                                   |
| Affected Component | Dubbo API Debug Interface             |
| Detection Method   | HTTP POST Request                     |

Reference:

* [https://www.secevery.com/toBugInfo?id=2033835475254124546](https://www.secevery.com/toBugInfo?id=2033835475254124546)

---

## Technical Summary

The target application exposes a debug endpoint:

```text
/papi/esearch/data/devops/dubboApi/debug/method
```

The PoC attempts to invoke:

```text
cn.hutool.core.util.RuntimeUtil.execForStr
```

with attacker-controlled input.

If the endpoint is accessible and vulnerable, arbitrary system commands may be executed on the remote host.

The provided script validates exploitation success by executing:

```bash
id
```

and checking whether the response contains:

```text
uid=
```

---

## Features

* Multi-threaded target scanning
* Batch processing from file input
* Colored terminal output
* Vulnerability verification logic
* Timeout/error handling
* Automatic logging of successful results

---

## Repository Structure

```text
.
├── QVD-2026-14149.py      # Main PoC script
├── QVD-2026-14149.txt     # Target list
└── README.md              # Documentation
```

---

## Requirements

### Python Version

The original script is written for:

```text
Python 2.x
```

Recommended:

```bash
Python 2.7
```

### Dependencies

Install required modules:

```bash
pip install requests
```

---

## Input File Format

The target list file should contain one target per line.

Example:

```text
https://target1.com
http://192.168.1.10:8080
https://example.org
```

The provided sample target file contains numerous example endpoints. fileciteturn0file0

---

## Usage

### Run the Script

```bash
python2 QVD-2026-14149.py
```

You will be prompted for the target list:

```text
 - [WEBLIST] > targets.txt
```

---

## Detection Logic

The script:

1. Reads targets from the provided file
2. Sends a crafted POST request to the Dubbo debug endpoint
3. Attempts command execution using:

```text
RuntimeUtil.execForStr
```

4. Verifies successful execution by checking for:

```text
uid=
```

5. Stores successful results in:

```text
SAHMSEC_QVD-2026-14149-results.txt
```

---

## Example Output

```text
- https://target.com --> Exploited
- Id : uid=0(root) gid=0(root)
```

Non-vulnerable targets:

```text
- https://target.com --> Not_Vulnerable
```

Timeout or unreachable hosts:

```text
- https://target.com --> Time0ut
```

---

## Important Notes

* SSL verification is disabled in the script.
* The script uses 20 concurrent threads.
* Responses are parsed using regular expressions.
* Successful targets are appended to an output file.
* The PoC currently executes only the `id` command for validation.

---

## Indicators of Exposure

The following FOFA query may help identify exposed systems:

```text
icon_hash="-1619753057"
```

---

## Security Recommendations

If you manage a potentially affected Weaver E-cology10 instance:

* Disable exposed debug interfaces
* Restrict public access to internal APIs
* Apply vendor patches immediately
* Place the application behind VPN or WAF protections
* Monitor suspicious requests to:

```text
/papi/esearch/data/devops/dubboApi/debug/method
```

* Audit server logs for unexpected command execution activity

---

## Disclaimer

This project is intended solely for defensive security research and authorized testing.

The author is not responsible for:

* Misuse of the software
* Unauthorized access attempts
* Damage caused by improper usage
* Legal consequences resulting from abuse

Use responsibly and only within environments where you have explicit permission.

---

## Source Information

Primary PoC source code analyzed and rebranded for SAHM
