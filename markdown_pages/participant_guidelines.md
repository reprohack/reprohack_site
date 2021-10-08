> **As all ReproHack events, we strive to make this event open and inclusive
to all. As such the event is governed by the [ReproHack Code of
Conduct](code-of-conduct.html)
and you should read it before participating. By participating, you are
expected to uphold this code.**


We are all excited by the progress made by many authors to **make their
papers reproducible by publishing associated code and data**.

We know how challenging it can be so we **want to showcase the value of
the practice**, both for original authors and as a learning experience
for those who attempt to reproduce the work.

It’s imperative to note that **ReproHacks are by no means an attempt to
criticise or discredit work**. We see reproduction as **beneficial
scientific activity in itself**, with useful outcomes for authors and
valuable learning experiences for the participants and the research
community as a whole.

-----

### Overall ReproHack Objectives

1. **Practical Experience in Reproducibility**

3. **Giving feedback to Authors**

5. **Thinking more broadly about opportunities and challenges associated with Research Reprodicibility**

<figure>
<img src="/static/images/1728_TURI_Book sprint_7 community_040619.jpg" width=40%>
<figcaption> The Turing Way Community, & Scriberia. (2019, July 11). Illustrations from the Turing Way book dashes. <a href=http://doi.org/10.5281/zenodo.3332808>doi.org/10.5281/zenodo.3332808</a>  </figcaption> </figure>

### Considerations when Reviewing

In addition to complying to the **[ReproHack Code of Conduct](code-of-conduct.html)**, please also consider the following when developing your feedback to the authors:

- #### Reproducibility is hard!
  Authors submitting their materials for us to work with are incredibly brave. Often, it might be the first time that someone else has attempted to reproduce their work so things that might be obviously missing from a reviewers point of view might have been impossible to pick up.

- #### Without them there would be no ReproHack. 
  Indeed, without the authors putting their materials forward, there would be nothing for us to work with and learn from! So do show gratitude and appreciation for their efforts to open up their work. 
- #### Constructive criticism only please!
    The purpose of a ReproHack is not to tear other people's work down. It is for all of us to learn by interacting with the materials. So please make sure your feedback is not personal or unecessarily critical. Instead, try to focus on your perspective, conveying any difficulties you experienced and offering suggestions on how your experiences with the materials could be improved. 


Ultimately, the purpose of the events is to make science better for all.

## Tips for Reproducing & Reviewing

### Selecting Papers

There are a number of strategies and information available to you to help you select a paper to work on:

- #### Focus on papers associated with your event
  If the event you are attending has a particular theme, you may want to focus on papers submitted specifically for that event. A list of such associated papers will appear at the bottom of your event page. 
- #### Explore central paper list
  The full list of papers submitted to the hub can be found on our **[Papers](paper)** page. You can **search** the list for specific terms or **filter papers by tags** relating to the **domain** or **tools and languages** used (for example, you could focus on papers that use R or python as their analysis language).

- #### Use information supplied by the author
  This includes a **short description** of the paper, a pitch for **why you should attempt to reproduce it**, tips on **what to focus on** when reviewing and **tags** indicating the domain or **tools and languages** used.

- #### Use paper metrics
  Any paper that has already been reviewed will have the **number of reviews** and **mean reproducibility score** displayed. This metric is in *no way standardised, can be quite subjective* and also reflects reviewers familiarity with the tools and methods used by the authors, so it is **not a standardised and objective reflection of quality of the effort**. However, they can be useful as an indicator of potential level of challenge. For example, a higher reproducibility score could present a slightly easier experience for a wider range of participants. If you are up for a challenge, you could try a paper with a lower score. Or, even better, you could venture into the unknown and select a paper that has not been reviewed yet! You will learn something whatever you choose! 

Once you've selected your paper, rememeber to register your selection in the hackpad using the following template:

    ### **Paper:** <Title of the paper reproduced>
    **Reviewers:** Reviewer 1, Reviewer 2 etc.

### Reviewing as an auditor

Auditing is defined as the verification activity of a process or quality system, to ensure compliance to requirements. In the case of reproducible research, what we are aiming for broadly is to produce **materials that are FAIR (findable, accessible, interoperable and reusable)**.

<figure>
<img src="/static/images/1728_TURI_Book sprint_8 FAIR principles_040619.jpg" width=50%>
<figcaption> The Turing Way Community, & Scriberia. (2019, July 11). Illustrations from the Turing Way book dashes. <a href=http://doi.org/10.5281/zenodo.3332808>doi.org/10.5281/zenodo.3332808</a>  </figcaption> </figure>

Here's some tips on more specific aspects of the materials to focus on:

#### Access

- How **easy** was it to **gain** access to the materials?

- Did you manage to download all the files you needed?

]

#### Installation

- How **easy / automated** was **installation**?

- Did you have any problems?

- How did you solve them?


#### Data

- Were **data clearly separated from code and other items**?

- Were **large data files deposited in a trustworthy data repository** and referred to using a **persistent identifier**?

- Were **data documented** ...somehow...

#### Documentation

Was there **adequate documentation** describing:
- how to **install** necessary software including non-standard dependencies?

- how to **use** materials to reproduce the paper?

- how to **cite** the materials, ideally in a form that can be copy and pasted?
#### Analysis

- **Were you able to fully reproduce** the paper? `r emo::ji("white_check_mark")`

- **How automated** was the process of reproducing the paper?

- **How easy was it to link** analysis **code** to:
   - the **plots** it generates
   - **sections in the manuscript** in which it is described and results reported


#### If the analysis was not fully reproducible 

 - Were there **missing dependencies?**
 
 - Was the **computational environment not adequately described** / captured?
 
 - Was there **bugs** in the code?
 
 - Did **code run but results (e.g. model outputs, tables, figures) differ** to those published? By **how much?**


### Transparency 

- How easy was it to navigate the materials?
- How easy was it to find the code the generated specific results (plot, table, reported statistic)?
