===========
RFM Package
===========


.. image:: https://img.shields.io/pypi/v/rfm_segmentation.svg
        :target: https://pypi.python.org/pypi/rfm_segmentation

.. image:: https://img.shields.io/travis/Esmila/rfm_segmentation.svg
        :target: https://travis-ci.com/Esmila/rfm_segmentation

.. image:: https://readthedocs.org/projects/rfm-segmentation/badge/?version=latest
        :target: https://rfm-segmentation.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




RFM Package for Customer Segmentation


* Free software: MIT license
* Documentation: https://rfm-segmentation.readthedocs.io.


Features
--------

* def rfm_score_generator(data,totalPaid, day_bought,customerID, invoiceNo = "", format_ = '%d.%m.%Y', R_w=0.15, F_w=0.28, M_w =0.57):
   

    Parameters
    ----------
    data : the data of customers you want to segment
        
    totalPaid : the monetary value (quantity * unit_price)
        
    day_bought : the date of the purchase
        
    customerID : unique identifier for  each customer
        
    invoiceNo : unique identifier for each purchase
         (Default value = ""), if missing take date of each purchase
    format_ : the date format for day_bought column
         (Default value = '%d.%m.%Y')
    R_w : the weight given to Recency to calculate RFM Score
         (Default value = 0.15)
    F_w : the weight given to Frequency to calculate RFM Score
         (Default value = 0.28)
    M_w : the weight given to Monetary value to calculate RFM Score
         (Default value = 0.57)

    Returns
    The RFM (dataframe) with added columns of Recency, Freqency, Monetary Ranks both normalized and not normalized, RFM Score, and the Segment the Customer belongs to, e.g Loyal customer.
    The Maximum RFM Score is 5.
* 
*

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
