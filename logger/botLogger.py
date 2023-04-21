import logging

class botLogger:
    def getLogger(name):
        
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(module)s;%(lineno)d;%(message)s")
        
        handler = logging.FileHandler(f'logs/{name}.log')
        handler.setFormatter(formatter)
        
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.propagate = True
        
        return logger
        
        